import cadquery as cq

# Parameters for the model
length = 150.0          # Total length of the bracket
height = 20.0           # Height of the vertical web
width_max = 35.0        # Maximum width of the triangular flange
thickness = 2.0         # Material thickness
slot_width = 3.0        # Width of the rectangular cutouts
slot_height = 8.0       # Height of the rectangular cutouts
slot_pitch = 6.0        # Distance between slot centers
num_slots = 20          # Number of slots
start_offset = 15.0     # Distance from left edge to first slot
gap_between_parts = 15.0 # Vertical gap for the exploded view

# 1. Create the Main Body (Upper Bracket)

# Create the Vertical Web (Front Face)
# Oriented on the XZ plane, extruded in +Y (thickness)
# Position: X from 0 to length, Z from -height to 0, Y from 0 to thickness
web = (cq.Workplane("XY")
       .workplane(offset=0)
       .moveTo(0, 0)
       .rect(length, thickness, centered=False)
       .extrude(-height)
      )

# Create the Horizontal Flange (Top Face)
# Triangular shape attached to the back of the web
# Position: Z from 0 to -thickness (flush with top), Y starting from thickness
flange_pts = [
    (0, thickness),
    (length, thickness),
    (0, width_max)
]

flange = (cq.Workplane("XY")
          .polyline(flange_pts)
          .close()
          .extrude(-thickness)
         )

# Combine Web and Flange
main_body = web.union(flange)

# Add Fillet to the internal corner
# The edge is along the X axis, located at Y=thickness, Z=-thickness
# We select edges that are "inside" the bounding box of the connection
try:
    main_body = main_body.edges(
        cq.selectors.BoxSelector(
            (-1, thickness - 0.1, -thickness - 0.1),
            (length + 1, thickness + 0.1, -thickness + 0.1)
        )
    ).fillet(thickness / 2.0)
except:
    # Fallback if selection is tricky, though coordinates are deterministic
    pass

# Create the Cutouts (Slots) on the Vertical Web
# We create a single cutter and pattern it, or iterate
for i in range(num_slots):
    x_pos = start_offset + (i * slot_pitch)
    
    # Define cutter box
    # Center X at x_pos
    # Z range: from bottom (-height) up to (-height + slot_height)
    # Y range: needs to cut through the web (0 to thickness)
    
    # Using a Workplane on the front face (Y=0)
    slot_cutter = (cq.Workplane("XZ")
                   .workplane(offset=-1) # Start slightly in front
                   .moveTo(x_pos, -height) # Bottom edge
                   .rect(slot_width, slot_height * 2, centered=True) # Tall rect centered on bottom edge
                   .extrude(thickness + 2) # Cut through
                  )
    
    main_body = main_body.cut(slot_cutter)

# Optional: Add a "nose" detail to the left of the web
# Chamfer the bottom-left corner of the web
main_body = main_body.edges(
    cq.selectors.NearestToPointSelector((0, 0, -height))
).chamfer(height * 0.4)


# 2. Create the Separate Bottom Strip (Exploded View Element)

# The strip mimics the web's slotted area
strip_length = (num_slots * slot_pitch) + 10
strip_start_x = start_offset - slot_pitch
strip_z_pos = -height - gap_between_parts

# Create base strip
strip = (cq.Workplane("XY")
         .workplane(offset=strip_z_pos)
         .moveTo(strip_start_x, 0)
         .rect(strip_length, thickness, centered=False)
         .extrude(-slot_height) # Extrude downwards
        )

# Cut matching slots from the top of the strip
for i in range(num_slots):
    x_pos = start_offset + (i * slot_pitch)
    
    slot_cutter = (cq.Workplane("XZ")
                   .workplane(offset=-1)
                   .moveTo(x_pos, strip_z_pos)
                   .rect(slot_width, slot_height, centered=True) # Center on top edge of strip
                   .extrude(thickness + 2)
                  )
    strip = strip.cut(slot_cutter)

# Combine both parts into the final result
result = main_body.union(strip)

# Export or display is handled by the environment invoking this script