import cadquery as cq

# Parametric dimensions based on visual estimation
length = 100.0  # Length of the block
width = 50.0    # Width of the block
thickness = 20.0 # Thickness/Height of the block

# Create the solid rectangular box centered on the XY plane
result = cq.Workplane("XY").box(length, width, thickness)