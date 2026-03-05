import cadquery as cq

# Define parameters for the model
length = 100.0  # Length of the bar
width = 10.0    # Width of the cross-section
height = 10.0   # Height of the cross-section
chamfer_size = 1.5  # Size of the 45-degree chamfer

# Create the CAD model
# 1. Start with a box (rectangular prism) centered on the XY plane
# 2. Select the longitudinal edge located at the top (>Z) and front (<Y)
# 3. Apply a chamfer to the selected edge
result = (
    cq.Workplane("XY")
    .box(length, width, height)
    .edges(">Z and <Y")
    .chamfer(chamfer_size)
)