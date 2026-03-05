import cadquery as cq

# Head tube
head_tube = cq.Workplane("XY").circle(20).extrude(60)

# Seat tube
seat_tube = cq.Workplane("XZ").circle(15).extrude(80).translate((0, 0, 60))

# Top tube
top_tube = cq.Workplane("XZ").lineTo(100, 0).threePointArc((80, -20), (110, -40)).close().sweep(cq.Workplane("YZ").circle(10))

# Down tube
down_tube = cq.Workplane("XZ").lineTo(90, 0).threePointArc((70, 40), (120, 80)).close().sweep(cq.Workplane("YZ").circle(12))

# Bottom bracket
bottom_bracket = cq.Workplane("XY").circle(15).extrude(30).translate((0, -15, 0))

# Joining all parts
result = head_tube.union(seat_tube).union(top_tube).union(down_tube).union(bottom_bracket)