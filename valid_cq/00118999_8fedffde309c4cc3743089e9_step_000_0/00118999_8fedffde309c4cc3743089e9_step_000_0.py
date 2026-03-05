import cadquery as cq

# Define parametric dimensions based on visual proportions
height = 100.0  # Vertical dimension
width = 60.0    # Horizontal dimension of the large face
thickness = 15.0 # Depth/thickness of the plate

# Create the rectangular prism (box)
# The box is created on the XY plane, with dimensions aligned to X (width), Y (thickness), and Z (height)
result = cq.Workplane("XY").box(width, thickness, height)