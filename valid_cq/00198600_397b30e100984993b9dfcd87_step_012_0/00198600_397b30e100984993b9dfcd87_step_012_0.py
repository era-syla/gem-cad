import cadquery as cq

# Parametric dimensions based on the visual proportions of the image
height = 100.0  # Vertical dimension
width = 20.0    # Width of the face
thickness = 5.0 # Thickness of the plate

# Create a rectangular prism (box)
# The box is centered on the origin
result = cq.Workplane("XY").box(width, thickness, height)