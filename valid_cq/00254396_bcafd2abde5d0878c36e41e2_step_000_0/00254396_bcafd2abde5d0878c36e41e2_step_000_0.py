import cadquery as cq

# Parametric dimensions based on the visual aspect ratio of the image
# Estimated ratio: Length ~3-4x Width, Width ~6x Thickness
length = 100.0
width = 30.0
thickness = 5.0

# Create a simple rectangular prism (box)
# The box is centered on the origin by default
result = cq.Workplane("XY").box(length, width, thickness)