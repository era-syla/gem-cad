import cadquery as cq

# Parametric dimensions based on visual estimation
length = 120.0  # Length of the plate (X axis)
height = 40.0   # Height of the plate (Z axis)
thickness = 5.0 # Thickness of the plate (Y axis)

# Create the rectangular plate geometry
# Using the XY workplane and creating a box centered at the origin
result = cq.Workplane("XY").box(length, thickness, height)