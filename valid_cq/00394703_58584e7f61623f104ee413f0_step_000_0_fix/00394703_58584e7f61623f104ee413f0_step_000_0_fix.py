import cadquery as cq

# Main body
body = (cq.Workplane("XY")
        .box(20, 20, 5)
        .faces(">Z").workplane()
        .rect(10, 10)
        .cutBlind(-2))

# Arms
arm = (cq.Workplane("XY")
       .center(10, 0)
       .slot2D(50, 10)
       .extrude(5)
       .faces(">Z").workplane()
       .rect(20, 5)
       .cutBlind(-2))

# Motor mounts
motor_mount = (cq.Workplane("XY")
               .circle(5)
               .extrude(5)
               .faces(">Z").workplane()
               .circle(3)
               .cutBlind(-5))

# Assembly
arm = arm.union(arm.rotate((0, 0, 0), (0, 0, 1), 90))
arm = arm.union(arm.rotate((0, 0, 0), (0, 0, 1), 180))
arm = arm.union(arm.rotate((0, 0, 0), (0, 0, 1), 270))

motor_mount = motor_mount.translate((25, 0, 0))
motor_mount = motor_mount.union(motor_mount.rotate((0, 0, 0), (0, 0, 1), 90))
motor_mount = motor_mount.union(motor_mount.rotate((0, 0, 0), (0, 0, 1), 180))
motor_mount = motor_mount.union(motor_mount.rotate((0, 0, 0), (0, 0, 1), 270))

result = body.union(arm).union(motor_mount)