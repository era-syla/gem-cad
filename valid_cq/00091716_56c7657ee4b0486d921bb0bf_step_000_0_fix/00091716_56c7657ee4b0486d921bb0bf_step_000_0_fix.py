import cadquery as cq

arm_length = 150
arm_width = 20
arm_thickness = 4
motor_hole_diameter = 10
fuselage_size = 50
fuselage_thickness = 4

arm = (
    cq.Workplane("XY")
    .center(-arm_length / 2, 0)
    .rect(arm_length, arm_width)
    .extrude(arm_thickness)
    .edges("|Z").fillet(2)
    .faces(">Z")
    .workplane()
    .center(-arm_length / 2, 0)
    .circle(motor_hole_diameter / 2)
    .cutThruAll()
)

fuselage = (
    cq.Workplane("XY")
    .rect(fuselage_size, fuselage_size)
    .extrude(fuselage_thickness)
)

result = (
    fuselage
    .union(arm)
    .union(arm.rotate((0, 0, 0), (0, 0, 1), 90))
    .union(arm.rotate((0, 0, 0), (0, 0, 1), 180))
    .union(arm.rotate((0, 0, 0), (0, 0, 1), 270))
)