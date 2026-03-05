import cadquery as cq

# Parametric dimensions
length = 200.0  # Length of the bar
width = 5.0     # Width of the cross-section
height = 5.0    # Height of the cross-section

# Create the rectangular bar geometry
# We use the box primitive which centers the object at the origin
result = cq.Workplane("XY").box(length, width, height)