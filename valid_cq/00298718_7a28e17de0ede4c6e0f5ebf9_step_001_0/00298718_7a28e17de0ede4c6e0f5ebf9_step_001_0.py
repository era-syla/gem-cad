import cadquery as cq

# Define parametric dimensions based on the visual proportions of the image
height = 80.0      # The vertical dimension (Z-axis)
width = 15.0       # The wider horizontal dimension (X-axis)
thickness = 8.0    # The narrower horizontal dimension (Y-axis)

# Create the rectangular prism (box)
# The box is created centered on the origin
result = cq.Workplane("XY").box(width, thickness, height)