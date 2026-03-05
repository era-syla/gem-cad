import cadquery as cq

# Parametric dimensions
length = 100.0  # Length of the square plate
width = 100.0   # Width of the square plate
thickness = 2.0 # Thickness of the plate

# Create the 3D model
# box() creates a centered rectangular prism on the current workplane
result = cq.Workplane("XY").box(length, width, thickness)