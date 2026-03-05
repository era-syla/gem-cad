import cadquery as cq

# Outer link plate
outer_plate = (
    cq.Workplane("XY")
    .rect(60, 10)
    .extrude(2)
    .faces(">Z")
    .workplane(centerOption="CenterOfBoundBox")
    .hole(5)
    .transformed(offset=cq.Vector(0, 50, 0))
    .hole(5)
)

# Inner link plate
inner_plate = (
    cq.Workplane("XY")
    .rect(50, 10)
    .extrude(2)
    .faces(">Z")
    .workplane(centerOption="CenterOfBoundBox")
    .hole(5)
    .transformed(offset=cq.Vector(0, 40, 0))
    .hole(5)
)

# Assembling the chain
result = (
    outer_plate
    .union(outer_plate.mirror("XY").translate((0, 0, 26)))
    .union(inner_plate.translate((0, 0, 12)))
    .union(inner_plate.mirror("XY").translate((0, 0, 14)))
)