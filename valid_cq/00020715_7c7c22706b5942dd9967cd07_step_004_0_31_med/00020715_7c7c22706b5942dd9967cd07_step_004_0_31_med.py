import cadquery as cq

# Parameters
base_radius = 15.0
base_height = 15.0

shaft_radius = 4.0
shaft_height = 50.0

head_radius = 13.0
head_height = 18.0

hole_radius = 3.5
hole_depth = 18.0

num_grooves = 12
groove_radius = 3.0
groove_offset = 13.5

# Create base
result = cq.Workplane("XY").circle(base_radius).extrude(base_height)

# Create middle shaft
result = result.faces(">Z").workplane().circle(shaft_radius).extrude(shaft_height)

# Create top head
result = result.faces(">Z").workplane().circle(head_radius).extrude(head_height)

# Cut knurling/grooves into the top head
result = (
    result.faces(">Z")
    .workplane()
    .polarArray(groove_offset, 0, 360, num_grooves)
    .circle(groove_radius)
    .cutBlind(-head_height)
)

# Cut the center hole in the top head
result = (
    result.faces(">Z")
    .workplane()
    .circle(hole_radius)
    .cutBlind(-hole_depth)
)