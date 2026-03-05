import cadquery as cq

# Define parametric dimensions based on visual estimation
# The object appears to be a long rectangular bar with a square cross-section
length = 200.0
width = 10.0
height = 10.0

# Create the rectangular prism
# box() generates a box centered at the origin
result = cq.Workplane("XY").box(length, width, height)