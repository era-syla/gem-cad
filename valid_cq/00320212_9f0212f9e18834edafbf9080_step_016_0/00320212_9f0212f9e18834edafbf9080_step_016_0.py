import cadquery as cq

# Define parametric dimensions
length = 100.0
width = 30.0
height = 30.0
hole_diameter = 16.0

# Create the 3D model
# 1. Start on the YZ plane to sketch the cross-section
# 2. Draw the outer rectangle
# 3. Draw the inner circle to create the hollow center
# 4. Extrude along the X-axis to create the length of the bar
result = (
    cq.Workplane("YZ")
    .rect(width, height)
    .circle(hole_diameter / 2.0)
    .extrude(length)
)