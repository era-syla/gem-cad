import cadquery as cq

# Parametric dimensions
height = 100.0  # Length of the cylinder
radius = 5.0    # Radius of the cylinder

# Create the cylindrical rod
# We extrude a circle along the Z axis
result = (
    cq.Workplane("XY")
    .circle(radius)
    .extrude(height)
)

# Alternatively, a simpler way to create a cylinder directly:
# result = cq.Workplane("XY").cylinder(height, radius)