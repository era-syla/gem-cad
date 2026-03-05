import cadquery as cq

# Parametric dimensions
width = 10.0    # Width of the square cross-section
depth = 10.0    # Depth of the square cross-section
height = 200.0  # Height of the bar

# Create the vertical rectangular prism
result = (
    cq.Workplane("XY")
    .rect(width, depth)
    .extrude(height)
)