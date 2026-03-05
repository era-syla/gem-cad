import cadquery as cq

# Parametric dimensions based on visual estimation
length = 100.0  # Longest dimension
height = 20.0   # Vertical dimension
thickness = 5.0 # Depth dimension

# Create the rectangular prism (box)
# Aligned such that length is along X, thickness along Y, height along Z
result = cq.Workplane("XY").box(length, thickness, height)