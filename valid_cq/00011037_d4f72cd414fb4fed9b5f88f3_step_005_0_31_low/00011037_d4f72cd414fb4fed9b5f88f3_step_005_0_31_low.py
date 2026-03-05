import cadquery as cq

# Parameters
length = 100.0
height = 60.0
thickness = 10.0
chamfer_x = 30.0
chamfer_y = 40.0

# Create base block
base = cq.Workplane("XY").box(length, thickness, height)

# Apply chamfer
result = base.edges(">Z and <X").chamfer(chamfer_x, chamfer_y)
