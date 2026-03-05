import cadquery as cq

# Base block
block = cq.Workplane("XY").box(20, 10, 60)

# Cylindrical protrusion
cylinder = cq.Workplane("XY").workplane(offset=30).circle(10).extrude(20)

# Side arms
side_arm = cq.Workplane("XY").workplane(offset=35).rect(4, 20).extrude(3).edges("|Z").fillet(1)
side_arms = side_arm.translate((0, 12, 0)).union(side_arm.translate((0, -12, 0)))

# Top detail
top_detail = cq.Workplane("XY").rect(10, 4).extrude(10).translate((0, 0, 60))

# Combine all parts
result = block.union(cylinder).union(side_arms).union(top_detail)