import cadquery as cq

# Parameters
head_radius = 5.0
head_thickness = 2.0
shaft_radius = 2.0
shaft_length = 10.0
chamfer_size = 1.0

# Create the base part
result = (
    cq.Workplane("XY")
    .circle(head_radius)
    .workplane(offset=head_thickness)
    .circle(shaft_radius)
    .loft()
    .faces(">Z")
    .workplane()
    .circle(shaft_radius)
    .extrude(shaft_length)
    .edges(">Z")
    .chamfer(chamfer_size)
)
