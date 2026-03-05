import cadquery as cq

# Parameters for the model
outer_diameter = 60.0
height = 12.0
wall_thickness = 3.0
pocket_depth = 9.0
text_string = "CQ"
text_size = 22.0

# Create the base cylindrical cup
base_cylinder = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .extrude(height)
)

# Hollow out the center to create the pocket
cup_with_pocket = (
    base_cylinder
    .faces(">Z")
    .workplane()
    .circle((outer_diameter / 2.0) - wall_thickness)
    .cutBlind(-pocket_depth)
)

# Add stylized extruded text inside the pocket
# We offset the workplane down to the bottom of the pocket
# and extrude the text upwards to sit flush with the rim
result = (
    cup_with_pocket
    .faces(">Z")
    .workplane(offset=-pocket_depth)
    .text(text_string, text_size, pocket_depth, font="Arial", halign="center", valign="center")
)