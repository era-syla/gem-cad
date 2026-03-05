import cadquery as cq

motor = cq.Workplane("XY").workplane(offset=20).box(42, 42, 40)
coupler = cq.Workplane("XY").workplane(offset=40).cylinder(15, 4)
leadscrew = cq.Workplane("XY").workplane(offset=55).cylinder(180, 3)
carriage = cq.Workplane("XY").workplane(offset=62.5).box(30, 20, 15)
extrusion = (
    cq.Workplane("XY")
    .workplane(offset=70)
    .rect(12, 8)
    .extrude(200)
    .faces(">Y")
    .workplane()
    .rect(10, 3)
    .cutThruAll()
)
result = motor.union(coupler).union(leadscrew).union(carriage).union(extrusion)