import cadquery as cq

# Parametric dimensions based on the visual proportions of the image
length = 100.0  # The horizontal dimension
height = 80.0   # The vertical dimension
thickness = 20.0 # The depth dimension

# Create the rectangular solid
# Using the XY workplane and the box operation creates a centered cuboid
result = cq.Workplane("XY").box(length, thickness, height)