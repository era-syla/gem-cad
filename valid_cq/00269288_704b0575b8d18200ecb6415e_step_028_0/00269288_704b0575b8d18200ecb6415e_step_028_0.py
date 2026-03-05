import cadquery as cq

# Parametric dimensions based on visual estimation
length = 120.0  # Length of the plate
width = 40.0    # Width of the plate
thickness = 2.0 # Thickness of the plate

# Create the rectangular plate geometry
# Using box() creates a centered cuboid
result = cq.Workplane("XY").box(length, width, thickness)