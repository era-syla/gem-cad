import cadquery as cq

# Parametric dimensions based on visual estimation of the rectangular plate
length = 100.0  # Long edge dimension
width = 75.0    # Short edge dimension
thickness = 4.0 # Thickness of the plate

# Create the rectangular plate geometry
# We use the box method which creates a centered rectangular prism
result = cq.Workplane("XY").box(length, width, thickness)