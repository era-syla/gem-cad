import cadquery as cq

# --- Parametric Dimensions ---
# Main body dimensions
body_width = 60.0    # Approximate total width
body_depth = 25.0    # Approximate total depth
body_height = 8.0    # Main housing height
wall_thickness = 1.0

# Pin/Contact parameters
num_pins = 25        # Count based on visual estimation
pitch = 2.0          # Distance between pin centers
pin_width = 0.8
pin_thickness = 0.8
pin_extension_front = 3.0
pin_extension_back = 2.0

# Calculated width based on pins to make it centered
total_pin_span = (num_pins - 1) * pitch
# Adjust body width slightly to accommodate the pin array nicely
body_width = total_pin_span + 4.0 

# Inner cavity details
cavity_depth = 12.0
cavity_height = body_height - 2.5

# Step/Ledge details at the back
ledge_height = 3.0
ledge_depth = 6.0

# --- Modeling ---

# 1. Main Housing Body
# Create the base block
main_body = cq.Workplane("XY").box(body_width, body_depth, body_height)

# Create the internal cavity (where a PCB might slide in)
# We subtract a box from the front face
cavity = (cq.Workplane("XY")
          .workplane(offset=body_height/2)  # Start at top
          .center(0, -body_depth/2 + cavity_depth/2) # Align to front
          .box(body_width - 2*wall_thickness, cavity_depth, cavity_height)
          )

# Cut the cavity from the top front, but usually these are slots. 
# Looking at the image, it looks like a solid block with slots on top 
# and a stepped section at the back. Let's refine.

# Let's rebuild the main body shape as a profile to be extruded.
# Side profile view (YZ plane) looks like an 'L' shape or a stepped block.
# Points for side profile
pts = [
    (0, 0),
    (body_depth, 0),
    (body_depth, body_height),
    (ledge_depth, body_height), # Top back ledge
    (ledge_depth, body_height - 2.0), # Step down
    (0, body_height - 2.0), # Front top
    (0, 0) # Close loop
]

# We will create the complex body by combining a main block and cuts
# Base L-shape
housing = (cq.Workplane("YZ")
           .rect(body_depth, body_height, centered=False) # Basic block
           .workplane(offset=body_width/2) # Move to side to center extrusion later
           .extrude(body_width)
           .translate((-body_width/2, -body_depth/2, -body_height/2)) # Center it
           )

# Create the top step (the lower section at the front)
# Actually, looking closer, the front is lower than the back.
# Let's cut the front top section away.
cut_box = (cq.Workplane("XY")
           .workplane(offset=body_height/2)
           .center(0, -body_depth/2 + (body_depth - ledge_depth)/2)
           .box(body_width + 1, body_depth - ledge_depth, 2.5)
           )
housing = housing.cut(cut_box)

# Create the bottom extension (legs/standoffs) seen on the left and right edges in some connectors,
# but here it looks like a continuous bar at the bottom back? 
# The image shows a downward protrusion at the back.
back_leg = (cq.Workplane("XZ")
            .workplane(offset=body_depth/2 - 1.5)
            .center(0, -body_height/2)
            .box(body_width, 3.0, 4.0)
            )
housing = housing.union(back_leg)


# 2. Pin Slots and Contacts
# The image shows slots on top and metal pins.

# Create a single pin profile
# The pin goes through the body, sticks out the front, and bends down at the back.
pin_path = (cq.Workplane("YZ")
            .moveTo(pin_extension_front, body_height/2 - 1.0) # Start front
            .lineTo(-body_depth + ledge_depth, body_height/2 - 1.0) # Go back
            .lineTo(-body_depth, body_height/2 - 1.0) # Further back
            .lineTo(-body_depth - 2.0, body_height/2 - 3.0) # Bend down (angled)
            .lineTo(-body_depth - 2.0, -body_height/2 - 2.0) # Straight down
            )

# Let's model the pin as a simple rectangular solid for robustness
# Contact strip on top surface
pin_top_segment = (cq.Workplane("XY")
                   .box(pin_width, body_depth - 2.0, pin_thickness)
                   .translate((0, 0, body_height/2 - 1.0 - pin_thickness/2))
                   )

# The pins sticking out the front (comb-like structure)
front_pins = (cq.Workplane("XY")
              .box(pin_width, pin_extension_front, pin_thickness)
              .translate((0, -body_depth/2 - pin_extension_front/2, body_height/2 - 2.5))
              )

# The angled tails at the back
# Simplified as a vertical block for the back tail
back_tails = (cq.Workplane("YZ")
              .workplane(offset=0)
              .moveTo(body_depth/2, 0)
              .rect(3.0, 6.0, centered=True) # Approximate shape of the tail
              .extrude(pin_width)
              .translate((-pin_width/2, body_depth/2 + 1.5, -body_height/2 + 1.0))
              # Rotate to align with YZ plane properly
              .rotate((0,0,0), (1,0,0), 0) 
              .rotate((0,0,0), (0,1,0), 90)
              .rotate((0,0,0), (0,0,1), 90)
             )
# Correcting orientation of back tails manually based on visual
back_tail_geo = (cq.Workplane("XY")
                 .box(pin_width, 3.0, 6.0)
                 .translate((0, body_depth/2 + 1.5, -body_height/2))
                 )


# Combine pin parts
single_pin = pin_top_segment.union(front_pins).union(back_tail_geo)

# Create the slots in the housing (cuts)
# The slots are slightly wider than the pins
slot_width = pin_width + 0.4
slot_cut = (cq.Workplane("XY")
            .box(slot_width, body_depth, 1.5)
            .translate((0, 0, body_height/2 - 0.75))
            )

# 3. Array generation
# We will create one compound object of all pins and one compound of all cuts
pins = cq.Assembly()
cuts = cq.Assembly()

for i in range(num_pins):
    offset_x = -total_pin_span/2 + i * pitch
    
    # Add pin
    pins.add(single_pin.translate((offset_x, 0, 0)))
    
    # Add cut
    cuts.add(slot_cut.translate((offset_x, 0, 0)))

# Extract shapes from assemblies (or union them in loop for simple solid)
all_pins_solid = single_pin.translate((-total_pin_span/2, 0, 0))
all_cuts_solid = slot_cut.translate((-total_pin_span/2, 0, 0))

for i in range(1, num_pins):
    offset_x = -total_pin_span/2 + i * pitch
    all_pins_solid = all_pins_solid.union(single_pin.translate((offset_x, 0, 0)))
    all_cuts_solid = all_cuts_solid.union(slot_cut.translate((offset_x, 0, 0)))

# 4. Final Boolean Operations
# Apply slots to housing
housing_slotted = housing.cut(all_cuts_solid)

# Add small holes on top of the pins/housing if visible (image has small dots/holes between ribs)
# Let's add the small alignment/mold holes on the top surface of the lower step
hole_dia = 0.6
holes = (cq.Workplane("XY")
         .workplane(offset=body_height/2 - 2.5) # On the lower step
         .rarray(pitch, 1, num_pins, 1)
         .circle(hole_dia/2)
         .extrude(-2.0)
         )

housing_final = housing_slotted.cut(holes)

# Combine Housing and Pins
result = housing_final.union(all_pins_solid)

# Add side supports/features seen on far left/right
# The image shows the housing extends slightly past the last pins
side_wall_l = (cq.Workplane("XY")
             .box(2.0, body_depth, body_height)
             .translate((-body_width/2 + 1.0, 0, 0))
             )
side_wall_r = (cq.Workplane("XY")
             .box(2.0, body_depth, body_height)
             .translate((body_width/2 - 1.0, 0, 0))
             )

# Clean up intersection
result = result.union(side_wall_l).union(side_wall_r)

# Final center adjustment to origin
result = result.translate((0,0, body_height/2))