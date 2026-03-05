import cadquery as cq

# Define parametric dimensions based on the visual proportions of the image
length = 100.0   # Length of the bar
height = 25.0    # Vertical height
thickness = 5.0  # Thickness of the material

# Create the rectangular prism (box)
# The box is centered at the origin (0,0,0) by default
result = cq.Workplane("XY").box(length, thickness, height)