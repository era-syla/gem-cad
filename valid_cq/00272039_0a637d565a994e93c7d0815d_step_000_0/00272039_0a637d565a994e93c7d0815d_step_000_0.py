import cadquery as cq

# Define parametric dimensions
rod_radius = 5.0
rod_length = 60.0

# Create a base cylinder oriented along the Z-axis
# We will reuse this geometry to create the other arms via rotation
base_cylinder = cq.Workplane("XY").circle(rod_radius).extrude(rod_length)

# Create the three orthogonal arms
# 1. Z-axis arm: The base cylinder itself
arm_z = base_cylinder

# 2. X-axis arm: Rotate the base cylinder 90 degrees around the Y-axis
# This moves the Z-aligned cylinder to align with the positive X-axis
arm_x = base_cylinder.rotate((0, 0, 0), (0, 1, 0), 90)

# 3. Y-axis arm: Rotate the base cylinder -90 degrees around the X-axis
# This moves the Z-aligned cylinder to align with the positive Y-axis
arm_y = base_cylinder.rotate((0, 0, 0), (1, 0, 0), -90)

# Union the three arms into a single solid geometry
# This creates the central corner intersection
structure = arm_x.union(arm_y).union(arm_z)

# Apply fillets to the ends of the arms to create the hemispherical caps
# We select the edges at the maximum X, Y, and Z coordinates.
# Using a radius slightly less than the rod radius (e.g., * 0.99) is a standard 
# practice to ensure robust fillet generation without topological singularities.
result = (
    structure
    .edges(">X").fillet(rod_radius * 0.99)
    .edges(">Y").fillet(rod_radius * 0.99)
    .edges(">Z").fillet(rod_radius * 0.99)
)