import cadquery as cq

# Define parametric dimensions based on visual proportions
height = 80.0     # The vertical dimension (Z-axis)
width = 40.0      # The wider horizontal dimension
thickness = 10.0  # The narrower horizontal dimension (depth)

# Create the rectangular prism (box)
# Using the XY workplane and creating a centered box
result = cq.Workplane("XY").box(width, thickness, height)