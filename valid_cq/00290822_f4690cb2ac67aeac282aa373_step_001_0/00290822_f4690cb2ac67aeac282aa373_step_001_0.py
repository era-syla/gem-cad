import cadquery as cq

# Define parametric dimensions based on visual aspect ratio
width = 10.0
depth = 10.0
height = 60.0

# Create the rectangular prism (box)
# We create a box on the XY plane with the specified dimensions
result = cq.Workplane("XY").box(width, depth, height)