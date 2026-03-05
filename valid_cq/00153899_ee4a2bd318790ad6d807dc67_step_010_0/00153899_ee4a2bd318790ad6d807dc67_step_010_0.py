import cadquery as cq

# Parametric dimensions to match the long, thin aspect ratio of the object
length = 250.0   # Total length of the strip/bar
width = 3.0      # Width of the cross-section
thickness = 1.0  # Thickness of the cross-section

# Create the geometry
# Using a box operation to create a rectangular prism centered at the origin
# This represents the long, thin straight strip shown in the image
result = cq.Workplane("XY").box(length, width, thickness)