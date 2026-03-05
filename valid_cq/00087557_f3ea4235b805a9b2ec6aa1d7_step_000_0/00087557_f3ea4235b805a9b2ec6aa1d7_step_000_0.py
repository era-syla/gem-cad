import cadquery as cq

# Parametric dimensions based on the visual aspect ratio
height = 100.0   # Vertical dimension
width = 25.0     # Horizontal width
thickness = 5.0  # Depth/Thickness

# Create the rectangular prism (box)
# We align the dimensions to match the orientation: Width (X), Thickness (Y), Height (Z)
result = cq.Workplane("XY").box(width, thickness, height)