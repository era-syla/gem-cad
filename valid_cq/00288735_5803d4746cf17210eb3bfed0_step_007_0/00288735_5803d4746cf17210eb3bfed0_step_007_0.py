import cadquery as cq

# Define parametric dimensions for the rectangular bar
length = 200.0  # Length of the bar
width = 5.0     # Width of the cross-section
height = 5.0    # Height of the cross-section

# Create the solid geometry
# We create a box centered at the origin on the XY plane
result = cq.Workplane("XY").box(length, width, height)