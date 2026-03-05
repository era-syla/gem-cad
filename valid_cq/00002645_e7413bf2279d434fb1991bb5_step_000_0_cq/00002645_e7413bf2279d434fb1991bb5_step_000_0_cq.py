import cadquery as cq

# Parametric dimensions for the box
length = 20.0  # Dimension along X axis
width = 10.0   # Dimension along Y axis
height = 5.0   # Dimension along Z axis

# Create a solid box centered at the origin
# Note: box(length, width, height) creates a box centered at (0,0,0) by default in some contexts, 
# but Workplane.box implies the current workplane center.
result = cq.Workplane("XY").box(length, width, height)