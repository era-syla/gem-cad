import cadquery as cq

# Parameters
base_length = 100.0
base_width = 30.0
base_thickness = 5.0

peg_radius = 7.5
peg_height = 45.0
peg_offset_x = -(base_length / 2.0) + (base_width / 2.0)

# Create the model
result = (
    cq.Workplane("XY")
    .box(base_length, base_width, base_thickness)
    .faces(">Z")
    .workplane()
    .center(peg_offset_x, 0)
    .circle(peg_radius)
    .extrude(peg_height)
)