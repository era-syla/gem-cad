import cadquery as cq

# Define parameters for dimensions based on visual aspect ratio
height = 100.0  # Vertical length
width = 15.0    # Width of the front face
thickness = 5.0 # Thickness of the object

# Create a rectangular prism (box) standing vertically
# The box method creates a solid centered at the origin
result = cq.Workplane("XY").box(width, thickness, height)