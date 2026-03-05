import cadquery as cq

# Parameter definitions
radius = 25.0  # Radius of the cylinder
height = 25.0  # Height of the cylinder

# Create the cylinder
# We use the Z-axis as the vertical axis
result = cq.Workplane("XY").circle(radius).extrude(height)

# Alternatively, a direct primitive approach could be used:
# result = cq.Workplane("XY").cylinder(height, radius)