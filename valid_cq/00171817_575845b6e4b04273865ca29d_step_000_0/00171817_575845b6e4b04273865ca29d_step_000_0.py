import cadquery as cq

# Parametric dimensions based on the visual proportions of the image
height = 80.0     # Vertical dimension
width = 50.0      # Horizontal dimension of the main face
thickness = 10.0  # Depth/Thickness of the plate

# Create the rectangular solid (box)
# Aligned so height is along the Z-axis, width along X, and thickness along Y
result = cq.Workplane("XY").box(width, thickness, height)