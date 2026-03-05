import cadquery as cq

# Parametric dimensions
width = 100.0      # Total width of the plate
height = 70.0      # Total height of the plate
thickness = 2.0    # Thickness of the material

# Create the 3D model
# We create a box centered on the XY plane.
# To match the vertical orientation in the image:
#   - X dimension corresponds to width
#   - Y dimension corresponds to thickness
#   - Z dimension corresponds to height
result = cq.Workplane("XY").box(width, thickness, height)