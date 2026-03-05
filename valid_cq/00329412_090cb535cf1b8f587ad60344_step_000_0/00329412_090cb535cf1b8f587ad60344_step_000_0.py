import cadquery as cq

# Parametric dimensions based on the visual proportions of the image
length = 100.0   # Long dimension along X
height = 30.0    # Vertical dimension along Z
thickness = 3.0  # Thin dimension along Y

# Create a simple rectangular prism (plate)
# We create a box centered at the origin
result = cq.Workplane("XY").box(length, thickness, height)