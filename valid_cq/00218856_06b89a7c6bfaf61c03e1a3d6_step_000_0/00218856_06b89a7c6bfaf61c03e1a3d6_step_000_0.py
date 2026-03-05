import cadquery as cq

# Parametric dimensions
width = 10.0      # Dimension along the X-axis
thickness = 10.0  # Dimension along the Y-axis
height = 80.0     # Dimension along the Z-axis

# Create the rectangular prism (bar)
# We start with a 2D rectangle on the XY plane and extrude it upwards
result = (
    cq.Workplane("XY")
    .rect(width, thickness)
    .extrude(height)
)