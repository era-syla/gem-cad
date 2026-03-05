import cadquery as cq

# Base object
base = cq.Workplane("XY").circle(20).extrude(10)

# Extrusion for arm
arm = cq.Workplane("XY").lineTo(0, 40).lineTo(60, 40).lineTo(40, 0).close().extrude(10)

# Union of base and arm
solid = base.union(arm)

# Hole in the base
solid = solid.faces(">Z").workplane().hole(10)

# Triangular cut in the arm
solid = solid.faces(">Z").workplane(centerOption="CenterOfBoundBox").center(30, 20).polygon(3, 15).cutThruAll()

result = solid