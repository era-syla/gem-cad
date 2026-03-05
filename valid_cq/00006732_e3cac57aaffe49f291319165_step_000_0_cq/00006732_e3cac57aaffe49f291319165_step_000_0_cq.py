import cadquery as cq

# Parametric dimensions
diameter = 5.0
length = 100.0

# Create the cylinder
# We'll create a cylinder centered on the origin, aligned with the Z-axis (default)
# then rotate it to match the general isometric appearance if needed, 
# but usually standard orientation (along X or Z) is preferred for base parts.
# Let's align it along the X-axis as it appears long in that direction.

result = cq.Workplane("YZ").circle(diameter / 2).extrude(length)

# Alternatively, using the simpler cylinder method directly on XY plane
# result = cq.Workplane("XY").cylinder(length, diameter / 2, centered=(True, True, True))