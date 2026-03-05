import cadquery as cq

# Parametric dimensions
height = 90.0
width = 30.0
depth = 30.0
hole_diameter = 12.0
hole_offset = 20.0  # Distance from the end (top or bottom) to the hole center

# Create the main rectangular block, centered at the origin
# Z-axis corresponds to the height
result = cq.Workplane("XY").box(width, depth, height)

# Create the top hole on the front face (Face >Y)
# The workplane is established on the face, centered at (0, 0, 0) relative to the face
# We shift the center up along the local Y axis (which corresponds to global Z)
result = result.faces(">Y").workplane().center(0, height/2 - hole_offset).hole(hole_diameter)

# Create the bottom hole on the right face (Face >X)
# We shift the center down along the local Y axis (which corresponds to global Z)
result = result.faces(">X").workplane().center(0, -height/2 + hole_offset).hole(hole_diameter)