import cadquery as cq

# --- Parameters ---
# Body dimensions (Approximating a NEMA 17 Stepper Motor)
motor_width = 42.0  # NEMA 17 standard width
motor_length = 48.0 # Typical length for a medium NEMA 17
chamfer_size = 3.0  # Corner chamfer

# Pilot (Circular raised face)
pilot_diameter = 22.0
pilot_height = 2.0

# Shaft dimensions
shaft_diameter = 5.0
shaft_length = 24.0

# Shaft flat (D-shaft) features
flat_length = 15.0
flat_depth = 0.5

# Shaft groove
groove_width = 0.8
groove_depth = 0.3
groove_pos_from_tip = 2.0

# Mounting holes
hole_spacing = 31.0 # Standard NEMA 17 spacing
hole_diameter = 3.0 # M3 tapping size approximation (or clearance)
hole_depth = 4.5

# --- Modeling ---

# 1. Main Body
# Create the square block centered on XY plane
body = cq.Workplane("XY").box(motor_width, motor_width, motor_length)

# Apply chamfers to the four vertical edges to create the octagonal-like profile
body = body.edges("|Z").chamfer(chamfer_size)

# 2. Pilot (Raised circular platform on top)
pilot = (
    body.faces(">Z")
    .workplane()
    .circle(pilot_diameter / 2)
    .extrude(pilot_height)
)

# 3. Shaft
shaft = (
    pilot.faces(">Z")
    .workplane()
    .circle(shaft_diameter / 2)
    .extrude(shaft_length)
)

# 4. Shaft Detail: D-cut (Flat)
# We need to cut a flat section off the shaft.
# We'll create a box that intersects the shaft area we want to remove.
flat_cut_distance = (shaft_diameter / 2) - flat_depth
# Start drawing on the top of the shaft
shaft_with_flat = (
    shaft.faces(">Z")
    .workplane()
    .center(0, flat_cut_distance + (shaft_diameter/2)) # Shift center to outside the radius
    .rect(shaft_diameter * 2, shaft_diameter) # Create a large rectangle to cut with
    .cutBlind(-flat_length) # Cut down into the shaft
)

# 5. Shaft Detail: Retaining Ring Groove
# Position relative to the tip of the shaft
groove_z_pos = (motor_length / 2) + pilot_height + shaft_length - groove_pos_from_tip

# Create a workplane at the groove height
groove_cutter = (
    cq.Workplane("XY")
    .workplane(offset=groove_z_pos)
    .circle(shaft_diameter / 2) # Outer diameter
    .circle((shaft_diameter / 2) - groove_depth) # Inner diameter
    .extrude(-groove_width) # Extrude downwards
)

# Subtract the groove ring from the main object
# Since 'groove_cutter' is a solid ring, we use cut()
result_no_holes = shaft_with_flat.cut(groove_cutter)

# 6. Mounting Holes
# Create holes on the top face of the main body (not the pilot)
# Note: Since the top face has been modified by the pilot extrusion, 
# it's safer to reference the original top Z level or pick the face carefully.
# Here we use the Z offset method for robustness.

top_z_level = motor_length / 2
result = (
    result_no_holes.faces(cq.NearestToPointSelector((0, 0, top_z_level)))
    .workplane()
    .rect(hole_spacing, hole_spacing, forConstruction=True)
    .vertices()
    .hole(hole_diameter, depth=hole_depth)
)

# Return result for visualization
if 'show_object' in globals():
    show_object(result)