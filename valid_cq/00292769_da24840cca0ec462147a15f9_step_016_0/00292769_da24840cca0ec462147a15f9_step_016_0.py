import cadquery as cq

# Define parametric dimensions based on the visual proportions of the image
length = 100.0  # Length of the plate
width = 40.0    # Width of the plate
thickness = 10.0 # Thickness of the plate

# Create a simple rectangular prism (box) centered on the XY plane
result = cq.Workplane("XY").box(length, width, thickness)