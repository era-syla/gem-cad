import cadquery as cq

# Define parametric dimensions based on visual proportions
length = 100.0  # Length of the box
width = 30.0    # Width of the box
height = 30.0   # Height of the box

# Create the rectangular prism (box)
# The box is centered on the origin by default
result = cq.Workplane("XY").box(length, width, height)