import cadquery as cq

arm_length = 100
arm_width = 8
end_diameter = 16
hole_diameter = 6

result = (
    cq.Workplane("XY")
    .circle(end_diameter / 2)
    .extrude(arm_width)
    .faces(">Z")
    .workplane()
    .center(arm_length, 0)
    .circle(end_diameter / 2)
    .extrude(arm_width)
    .faces("<Z[1]")
    .workplane()
    .rect(arm_length, arm_width)
    .extrude(arm_width)
    .faces(">Z")
    .workplane()
    .circle(hole_diameter / 2)
    .cutThruAll()
    .faces(">Z[1]")
    .workplane()
    .circle(hole_diameter / 2)
    .cutThruAll()
)