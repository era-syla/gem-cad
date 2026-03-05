import cadquery as cq

# Parametric dimensions based on visual estimation
length = 100.0  # Horizontal dimension
height = 50.0   # Vertical dimension
thickness = 5.0 # Depth dimension

# Create the rectangular box geometry
result = cq.Workplane("XY").box(length, height, thickness)