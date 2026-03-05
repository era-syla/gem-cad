import cadquery as cq

# Model parameters based on visual approximation
length = 120.0
height = 20.0
thickness = 3.0
chamfer_size = 8.0

# Generate the geometry
# 1. Create a rectangular base centered on the XY plane
# 2. Select the edge at the top-left corner (min X, max Y)
# 3. Apply a chamfer to create the angled cut
result = (
    cq.Workplane("XY")
    .box(length, height, thickness)
    .edges("<X and >Y")
    .chamfer(chamfer_size)
)