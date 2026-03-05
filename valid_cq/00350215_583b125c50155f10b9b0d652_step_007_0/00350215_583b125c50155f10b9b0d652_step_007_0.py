import cadquery as cq

# Define parametric dimensions based on visual proportions
length = 150.0  # Long dimension
width = 15.0    # Cross-section width
height = 15.0   # Cross-section height

# Create a rectangular prism (box) aligned with the axes
# This generates the long bar shape shown in the image
result = cq.Workplane("XY").box(length, width, height)