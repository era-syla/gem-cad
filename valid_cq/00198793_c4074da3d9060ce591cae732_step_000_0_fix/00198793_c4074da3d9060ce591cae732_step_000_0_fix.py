import cadquery as cq

# Create the base profile
base_profile = (
    cq.Workplane("XY")
    .moveTo(20, 0)
    .lineTo(40, 0)
    .threePointArc((50, 10), (40, 20))
    .lineTo(5, 20)
    .threePointArc((-5, 10), (5, 0))
    .close()
)

# Extrude the base profile
base = base_profile.extrude(3)

# Create the hole feature
hole = cq.Workplane("XY").circle(3).extrude(3)

# Position and cut the hole from the base
result = base.cut(hole.translate((30, 10, 0)))

# Create the arc and extrude for the top feature
arc_profile = (
    cq.Workplane("XY")
    .moveTo(35, 15)
    .threePointArc((45, 23), (35, 30))
    .close()
    .extrude(3)
)

# Combine the arc feature with the base
result = result.union(arc_profile)

# Create hole at the bottom
bottom_hole = cq.Workplane("XY").circle(2.5).extrude(3)
result = result.cut(bottom_hole.translate((13, 0, 0)))