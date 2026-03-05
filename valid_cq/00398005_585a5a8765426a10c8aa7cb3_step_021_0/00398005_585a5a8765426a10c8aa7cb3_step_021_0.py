import cadquery as cq

# Define parametric dimensions based on visual aspect ratio
length = 40.0  # Long dimension
width = 10.0   # Narrow dimension (depth)
height = 20.0  # Vertical dimension

# Create the rectangular prism (box)
# The box method creates a solid centered at the origin of the workplane
result = cq.Workplane("XY").box(length, width, height)