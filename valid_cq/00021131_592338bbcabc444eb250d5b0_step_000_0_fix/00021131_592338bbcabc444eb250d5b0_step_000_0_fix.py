import cadquery as cq

# Parameters
thickness = 8.0
outer_center_r = 20.0
outer_small_r = 10.0
small_center_x = 35.0
central_hole_r = 12.0
small_hole_r = 5.0

# Create the three lobes and fuse them
c1 = cq.Workplane("XY").circle(outer_center_r).extrude(thickness)
c2 = cq.Workplane("XY").circle(outer_small_r).extrude(thickness).translate(( small_center_x, 0, 0))
c3 = cq.Workplane("XY").circle(outer_small_r).extrude(thickness).translate((-small_center_x, 0, 0))

result = c1.union(c2).union(c3)

# Drill the central hole
result = result.workplane(offset=thickness).circle(central_hole_r).cutThruAll()

# Drill the two smaller holes
points = [( small_center_x, 0), (-small_center_x, 0)]
result = result.workplane(offset=thickness).pushPoints(points).circle(small_hole_r).cutThruAll()