import cadquery as cq

# Parametric dimensions based on visual aspect ratio estimation
length = 80.0   # Horizontal length
height = 50.0   # Vertical height
thickness = 20.0 # Depth/width

# Create a simple rectangular prism (box) centered at the origin
# box dimensions correspond to x, y, z axes
result = cq.Workplane("XY").box(length, thickness, height)