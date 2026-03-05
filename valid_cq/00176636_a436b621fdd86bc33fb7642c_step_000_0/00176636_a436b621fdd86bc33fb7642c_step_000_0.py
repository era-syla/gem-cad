import cadquery as cq

# Parametric dimensions for the cylinder
height = 100.0  # Total height of the rod
radius = 6.0    # Radius of the circular cross-section

# Create the cylindrical rod
# 1. Select the XY plane as the base
# 2. Draw a circle with the specified radius
# 3. Extrude the circle along the normal (Z-axis) by the height amount
result = cq.Workplane("XY").circle(radius).extrude(height)