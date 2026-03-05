import cadquery as cq

# Define parametric dimensions for the rectangular prism
length = 80.0  # Dimension along X-axis
width = 50.0   # Dimension along Y-axis
thickness = 10.0  # Dimension along Z-axis (height)

# Create the box geometry
# center=True is the default, centering the box at the origin
result = cq.Workplane("XY").box(length, width, thickness)