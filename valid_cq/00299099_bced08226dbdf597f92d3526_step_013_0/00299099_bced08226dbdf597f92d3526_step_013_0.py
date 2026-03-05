import cadquery as cq

# Define parametric dimensions based on visual estimation
length = 200.0  # Long dimension
width = 10.0    # Narrow dimension
thickness = 2.0 # Thickness

# Create a rectangular prism (box) centered on the XY plane
result = cq.Workplane("XY").box(length, width, thickness)