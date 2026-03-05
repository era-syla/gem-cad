import cadquery as cq

# Define parametric dimensions based on visual estimation
height = 100.0  # The vertical length of the strip
width = 10.0    # The wider face dimension
thickness = 2.0 # The narrow edge dimension

# Create the solid geometry (rectangular prism)
# We align the height with the Z-axis
result = cq.Workplane("XY").box(width, thickness, height)