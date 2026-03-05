import cadquery as cq

# Define parameters for the box dimensions
# These are estimated based on visual proportions of the provided image
length = 100.0  # X dimension
width = 100.0   # Y dimension
height = 20.0   # Z dimension (thickness)

# Create the rectangular prism (box)
# centered=True centers the box at the origin (0,0,0)
result = cq.Workplane("XY").box(length, width, height, centered=True)

# Alternatively, if you prefer corner alignment:
# result = cq.Workplane("XY").box(length, width, height, centered=False)