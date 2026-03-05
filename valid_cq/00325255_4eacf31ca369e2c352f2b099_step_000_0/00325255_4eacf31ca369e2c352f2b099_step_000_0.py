import cadquery as cq

# Define parametric dimensions based on visual proportions
width = 10.0   # Dimension along X-axis
depth = 10.0   # Dimension along Y-axis
height = 40.0  # Dimension along Z-axis (tall rectangular prism)

# Create the rectangular prism (box)
# The box is centered on the current workplane (XY) by default
result = cq.Workplane("XY").box(width, depth, height)