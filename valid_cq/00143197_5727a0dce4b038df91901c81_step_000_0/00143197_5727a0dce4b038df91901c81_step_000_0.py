import cadquery as cq

# Parametric dimensions for the model
total_length = 200.0
outer_diameter = 12.0
wall_thickness = 1.0

# Create the cylindrical body
# We start with a solid cylinder and then shell it to create the hollow tube structure.
# The shell operation with a negative thickness hollows the solid inwards.
# By selecting the top face (">Z") before shelling, that face is removed, leaving an open end.
# The bottom face remains closed, matching the appearance of the capped end in the image.
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .extrude(total_length)
    .faces(">Z")
    .shell(-wall_thickness)
)