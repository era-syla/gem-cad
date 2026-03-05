import cadquery as cq

# Parametric dimensions for the rectangular bar
length = 150.0  # Total length of the bar
width = 10.0    # Width of the cross-section
height = 10.0   # Height of the cross-section

# Create the 3D model
# box() creates a rectangular prism centered at the origin
result = cq.Workplane("XY").box(length, width, height)