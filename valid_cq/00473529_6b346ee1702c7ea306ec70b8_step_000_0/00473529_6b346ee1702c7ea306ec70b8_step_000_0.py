import cadquery as cq

# Parametric dimensions based on the visual proportions of the image
length = 100.0  # Length of the plate
width = 40.0    # Width of the plate
thickness = 2.0 # Thickness of the plate

# Create the rectangular plate geometry
# We use the box method to create a solid block centered at the origin
result = cq.Workplane("XY").box(length, width, thickness)