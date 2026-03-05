import cadquery as cq

# Parametric dimensions
length = 100.0   # Length of the block (X-axis)
height = 50.0    # Height of the block (Z-axis)
thickness = 15.0 # Thickness/Width of the block (Y-axis)
chamfer_size = 12.0 # Size of the chamfer on the bottom corners

# Create the 3D model
# 1. Start with a rectangular block centered on the XY plane
# 2. Select the bottom face (Z min)
# 3. From the bottom face, select the edges running parallel to the Y axis (the two ends)
# 4. Apply a chamfer to create the angled cuts at the bottom corners
result = (
    cq.Workplane("XY")
    .box(length, thickness, height)
    .faces("<Z")
    .edges("|Y")
    .chamfer(chamfer_size)
)