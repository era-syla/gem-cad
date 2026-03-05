import cadquery as cq

# Parametric dimensions based on visual proportions
height = 100.0  # Vertical dimension (Z axis)
width = 30.0    # Horizontal dimension (X axis)
thickness = 5.0 # Depth dimension (Y axis)

# Create a simple rectangular prism (box)
# The box method creates a box centered at the origin
result = cq.Workplane("XY").box(width, thickness, height)