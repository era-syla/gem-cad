import cadquery as cq

# Parametric dimensions based on the visual proportions of the image
length = 100.0  # Length of the plate
height = 20.0   # Height of the plate
thickness = 2.0 # Thickness of the plate

# Create the rectangular solid
# box() creates a rectangular prism centered at the origin
# Arguments correspond to dimensions along X, Y, and Z axes respectively
result = cq.Workplane("XY").box(length, thickness, height)