import cadquery as cq

# Define parametric dimensions based on the visual proportions of the image
# The object is a rectangular prism (bar)
length = 100.0  # Length along the main axis
width = 12.0    # Width (thickness)
height = 25.0   # Vertical height

# Create the solid geometry
# We use the XY workplane and create a centered box
result = cq.Workplane("XY").box(length, width, height)