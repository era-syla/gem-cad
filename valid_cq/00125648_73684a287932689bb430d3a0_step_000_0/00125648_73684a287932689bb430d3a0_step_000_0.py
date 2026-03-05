import cadquery as cq

# Parametric dimensions based on the visual proportions of the image
# The object is a long, thin rectangular bar
length = 200.0  # Long dimension
width = 10.0    # Intermediate dimension
height = 4.0    # Short dimension (thickness)

# Create the 3D model
# Workplane("XY") creates the base plane.
# box(length, width, height) creates a centered rectangular prism.
result = cq.Workplane("XY").box(length, width, height)