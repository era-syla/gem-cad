import cadquery as cq

# Build a sci-fi vehicle / heavy machinery model

# Main body - large central block
main_body = (
    cq.Workplane("XY")
    .box(80, 40, 30)
)

# Cab section - raised front portion
cab = (
    cq.Workplane("XY")
    .transformed(offset=(20, 0, 20))
    .box(35, 38, 20)
)

# Angled front nose of cab
nose = (
    cq.Workplane("XY")
    .transformed(offset=(38, 0, 12))
    .box(12, 36, 14)
)

# Rear engine/body extension
rear_body = (
    cq.Workplane("XY")
    .transformed(offset=(-30, 0, -2))
    .box(30, 32, 26)
)

# Lower chassis/underbody
chassis = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, -18))
    .box(90, 28, 8)
)

# Front left wheel assembly
wheel_fl = (
    cq.Workplane("YZ")
    .transformed(offset=(25, -8, 38))
    .circle(10)
    .extrude(10)
)

# Front right wheel assembly
wheel_fr = (
    cq.Workplane("YZ")
    .transformed(offset=(-15, -8, 38))
    .circle(10)
    .extrude(10)
)

# Rear left wheel
wheel_rl = (
    cq.Workplane("YZ")
    .transformed(offset=(25, -8, -30))
    .circle(10)
    .extrude(10)
)

# Rear right wheel
wheel_rr = (
    cq.Workplane("YZ")
    .transformed(offset=(-15, -8, -30))
    .circle(10)
    .extrude(10)
)

# Roof platform/deck
roof = (
    cq.Workplane("XY")
    .transformed(offset=(8, 0, 32))
    .box(50, 38, 4)
)

# Roof railing posts - front
rail_ff = (
    cq.Workplane("XY")
    .transformed(offset=(30, 16, 38))
    .box(2, 2, 12)
)
rail_fb = (
    cq.Workplane("XY")
    .transformed(offset=(30, -16, 38))
    .box(2, 2, 12)
)
rail_rf = (
    cq.Workplane("XY")
    .transformed(offset=(-12, 16, 38))
    .box(2, 2, 12)
)
rail_rb = (
    cq.Workplane("XY")
    .transformed(offset=(-12, -16, 38))
    .box(2, 2, 12)
)

# Railing top bars
rail_top_side_l = (
    cq.Workplane("XY")
    .transformed(offset=(9, 16, 44))
    .box(42, 2, 2)
)
rail_top_side_r = (
    cq.Workplane("XY")
    .transformed(offset=(9, -16, 44))
    .box(42, 2, 2)
)
rail_top_front = (
    cq.Workplane("XY")
    .transformed(offset=(30, 0, 44))
    .box(2, 32, 2)
)
rail_top_rear = (
    cq.Workplane("XY")
    .transformed(offset=(-12, 0, 44))
    .box(2, 32, 2)
)

# Turrets/cylinders on roof
turret1 = (
    cq.Workplane("XY")
    .transformed(offset=(5, 8, 36))
    .circle(5)
    .extrude(10)
)
turret2 = (
    cq.Workplane("XY")
    .transformed(offset=(5, -8, 36))
    .circle(5)
    .extrude(10)
)

# Front bumper/guard
bumper = (
    cq.Workplane("XY")
    .transformed(offset=(48, 0, 2))
    .box(6, 42, 18)
)

# Side exhausts/fins on left
fin_l = (
    cq.Workplane("XY")
    .transformed(offset=(-15, 20, 5))
    .box(25, 6, 20)
)

# Side exhausts/fins on right
fin_r = (
    cq.Workplane("XY")
    .transformed(offset=(-15, -20, 5))
    .box(25, 6, 20)
)

# Bottom skid block
skid = (
    cq.Workplane("XY")
    .transformed(offset=(-30, 0, -24))
    .box(20, 20, 6)
)

# Combine all parts
result = (
    main_body
    .union(cab)
    .union(nose)
    .union(rear_body)
    .union(chassis)
    .union(wheel_fl)
    .union(wheel_fr)
    .union(wheel_rl)
    .union(wheel_rr)
    .union(roof)
    .union(rail_ff)
    .union(rail_fb)
    .union(rail_rf)
    .union(rail_rb)
    .union(rail_top_side_l)
    .union(rail_top_side_r)
    .union(rail_top_front)
    .union(rail_top_rear)
    .union(turret1)
    .union(turret2)
    .union(bumper)
    .union(fin_l)
    .union(fin_r)
    .union(skid)
)