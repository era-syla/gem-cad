import cadquery as cq

# Define parametric dimensions for the box
length = 40.0  # Dimension along the X-axis
width = 20.0   # Dimension along the Y-axis
height = 10.0  # Dimension along the Z-axis

# Create the solid block
# centered=True centers the box at the origin (0,0,0) which is good practice
result = cq.Workplane("XY").box(length, width, height, centered=True)

# Alternatively, if not centered:
# result = cq.Workplane("XY").box(length, width, height, centered=False)