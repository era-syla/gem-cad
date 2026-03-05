import cadquery as cq

# Parametric dimensions based on the visual proportions of the image
length = 120.0   # Length of the plate (X axis)
height = 40.0    # Height of the plate (Z axis)
thickness = 4.0  # Thickness of the plate (Y axis)

# Create the rectangular solid (cuboid)
# We align the dimensions to stand upright as shown in the isometric view
result = cq.Workplane("XY").box(length, thickness, height)