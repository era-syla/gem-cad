import cadquery as cq

# Define parametric dimensions based on visual proportions
height = 60.0    # Vertical dimension
width = 30.0     # Horizontal dimension
thickness = 5.0  # Depth/Thickness dimension

# Create the rectangular prism (box)
# Using the XY workplane and extending in Z (height) to match the standing orientation
result = cq.Workplane("XY").box(width, thickness, height)