import cadquery as cq

# Create the base cylinder
base = cq.Workplane("XY").circle(10).extrude(20)

# Create the hexagonal nut shape
nut = cq.Workplane("XY").polygon(6, 25).extrude(10).translate((0, 0, 20))

# Create the sphere on top
sphere = cq.Workplane("XY").sphere(10).translate((0, 0, 35))

# Combine all parts
result = base.union(nut).union(sphere)

# Render the edges for filleting
result = result.edges("|Z").fillet(2.5)