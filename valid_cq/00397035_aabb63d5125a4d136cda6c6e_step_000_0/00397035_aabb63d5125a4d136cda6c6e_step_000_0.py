import cadquery as cq

# Define parametric dimensions
width = 100.0      # Dimension along the X axis
height = 60.0      # Dimension along the Z axis
thickness = 10.0   # Dimension along the Y axis

# Create the rectangular box geometry
# We use the XY workplane and the box operation to create a solid centered at the origin
result = cq.Workplane("XY").box(width, thickness, height)