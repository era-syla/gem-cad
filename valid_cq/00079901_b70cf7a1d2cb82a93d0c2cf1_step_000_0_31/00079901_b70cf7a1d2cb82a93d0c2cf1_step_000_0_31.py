import cadquery as cq

# Parametric dimensions
length = 100.0
width = 60.0
height = 25.0

left_pad_len = 40.0
cut_radius = 20.0
cut_center_x = left_pad_len + cut_radius

hole_radius = 10.0
hole_center_x = left_pad_len / 2.0

chamfer_size = 12.0

# Create base block and apply chamfers to the front corners
result = (
    cq.Workplane("XY")
    .box(length, width, height, centered=(False, True, False))
    .edges("<X and |Z")
    .chamfer(chamfer_size)
)

# Add the through hole
result = (
    result.faces(">Z")
    .workplane(centerOption="CenterOfBoundBox")
    .center(-length / 2.0 + hole_center_x, 0)
    .hole(hole_radius * 2.0)
)

# Create the semi-cylindrical cut tool
cut_tool = (
    cq.Workplane("XZ")
    .center(cut_center_x, height)
    .circle(cut_radius)
    .extrude(width * 1.5, both=True)
)

# Subtract the cut tool from the main body
result = result.cut(cut_tool)