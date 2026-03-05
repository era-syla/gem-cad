import cadquery as cq

# Left Component
left_part = cq.Workplane("XY").circle(50).extrude(10).faces(">Z").workplane().circle(40).cutThruAll()

# Right Component
right_part = cq.Workplane("XY").circle(50).extrude(10).faces(">Z").workplane().circle(40).cutThruAll().rotate((0, 0, 0), (0, 0, 1), 30)

# Center Component
center_part = (cq.Workplane("XY")
               .polygon(3, 60)
               .extrude(10)
               .faces(">Z")
               .workplane()
               .hole(20)
               .edges("|Z")
               .fillet(3))

# Combine all components
result = left_part.union(right_part).union(center_part)