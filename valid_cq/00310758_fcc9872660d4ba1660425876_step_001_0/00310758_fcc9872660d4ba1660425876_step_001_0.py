import cadquery as cq

# Parametric dimensions based on visual estimation of aspect ratio
# The object appears to be a square prism (rectangular bar)
width = 10.0   # Dimension along X axis
depth = 10.0   # Dimension along Y axis
height = 60.0  # Dimension along Z axis (Height)

# Create the rectangular prism centered at the origin
result = cq.Workplane("XY").box(width, depth, height)