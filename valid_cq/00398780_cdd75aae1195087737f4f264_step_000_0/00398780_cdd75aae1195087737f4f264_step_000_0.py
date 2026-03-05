import cadquery as cq

# Define parametric dimensions based on the visual aspect ratio
length = 100.0  # Long dimension
width = 50.0    # Short dimension
thickness = 10.0 # Thickness of the plate

# Create the rectangular solid
# The box method creates a rectangular prism centered at the origin
result = cq.Workplane("XY").box(length, width, thickness)