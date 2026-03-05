import cadquery as cq

# Parameters for the cylinder dimensions
radius = 10.0
height = 40.0

# Create the cylinder geometry
# 1. Initialize a Workplane on the XY plane
# 2. Draw a circle 2D profile
# 3. Extrude the profile to create a solid cylinder
result = cq.Workplane("XY").circle(radius).extrude(height)