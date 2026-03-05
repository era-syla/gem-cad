import cadquery as cq

# Parametric dimensions
main_body_length = 40.0
main_body_width = 20.0
main_body_height = 30.0

wing_length = 10.0  # How far they stick out
wing_width = main_body_width
wing_height = 5.0   # Thickness of the wing
wing_offset_from_top = 10.0 # Distance from top face to top of wing

# Create the main central block
# We center it on X and Y to make symmetry easier
main_body = cq.Workplane("XY").box(main_body_length, main_body_width, main_body_height)

# Calculate the Z position for the wings
# If box is centered at Z=0, top is at height/2.
# We want the top of the wing to be at (height/2) - wing_offset_from_top
# But cq.box centers the object, so we need to account for half the wing height.
wing_center_z = (main_body_height / 2.0) - wing_offset_from_top - (wing_height / 2.0)

# Create the wings
# We can make one long box that cuts through or extends past both sides
total_wing_span = main_body_length + (2 * wing_length)
wings = (
    cq.Workplane("XY")
    .workplane(offset=wing_center_z)
    .box(total_wing_span, wing_width, wing_height)
)

# Combine the main body and the wings
result = main_body.union(wings)