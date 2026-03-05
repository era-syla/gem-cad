import cadquery as cq

# Parametric dimensions based on visual estimation
length = 100.0  # Length of the plate
width = 25.0    # Width of the plate
thickness = 2.0 # Thickness of the plate

# Create the rectangular plate
# We create a box centered on the XY plane
result = cq.Workplane("XY").box(length, width, thickness)