import cadquery as cq

# Parametric dimensions based on the visual aspect ratio
length = 150.0  # Length of the plate
width = 100.0   # Width of the plate
thickness = 5.0 # Thickness of the plate

# Create the rectangular plate geometry
# Utilizing the box method which centers the geometry at the origin
result = cq.Workplane("XY").box(length, width, thickness)