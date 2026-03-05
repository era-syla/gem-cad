import cadquery as cq

# Define parametric dimensions based on the visual proportions of the image
# The object is a long, thin, flat rectangular bar
length = 200.0   # Length along the X-axis
height = 20.0    # Vertical height along the Z-axis
thickness = 4.0  # Thickness/depth along the Y-axis

# Create the rectangular solid
# box(length, width, height) creates a box centered at the origin
result = cq.Workplane("XY").box(length, thickness, height)