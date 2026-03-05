import cadquery as cq

# Parametric dimensions based on visual estimation of the provided image
length = 100.0  # Long dimension
width = 30.0    # Short dimension (depth)
height = 40.0   # Vertical dimension

# Create the rectangular cuboid (box)
# Centered at origin by default
result = cq.Workplane("XY").box(length, width, height)