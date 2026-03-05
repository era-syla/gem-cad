import cadquery as cq

# Parameters
big_radius = 20
small_radius = 10
center_distance = 30
thickness = 8
hole_diameter = 5

# Create the large cylinder
big_cyl = cq.Workplane("XY").circle(big_radius).extrude(thickness)

# Create the small cylinder offset along X
small_cyl = cq.Workplane("XY").center(center_distance, 0).circle(small_radius).extrude(thickness)

# Combine the two cylinders
result = big_cyl.union(small_cyl)

# Drill a hole through the large cylinder
result = result.faces(">Z").workplane().center(0, 0).hole(hole_diameter)