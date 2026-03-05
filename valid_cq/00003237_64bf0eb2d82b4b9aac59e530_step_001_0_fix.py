import cadquery as cq

# Model a simplified RC engine crankcase with cylinder head
# Main components: crankcase body, cylinder barrel, intake/exhaust ports

# --- Crankcase body (main block) ---
crankcase = (
    cq.Workplane("XY")
    .box(50, 45, 38)
)

# Round the crankcase edges
crankcase = (
    crankcase
    .edges("|Z")
    .fillet(6)
    .edges("#Z")
    .fillet(3)
)

# --- Cylinder barrel (vertical, sits on top of crankcase) ---
barrel_od = 28
barrel_id = 20
barrel_h = 42

cylinder = (
    cq.Workplane("XY")
    .workplane(offset=19)  # top of crankcase
    .circle(barrel_od / 2)
    .extrude(barrel_h)
)

# Cooling fins on barrel
fins = cq.Workplane("XY").workplane(offset=21)
fin_result = cq.Workplane("XY")
for i in range(8):
    z_off = 21 + i * 4.5
    fin = (
        cq.Workplane("XY")
        .workplane(offset=z_off)
        .circle((barrel_od + 8) / 2)
        .circle(barrel_od / 2)
        .extrude(2.0)
    )
    fin_result = fin_result.union(fin)

cylinder_with_fins = cylinder.union(fin_result)

# Hollow the cylinder
cylinder_bore = (
    cq.Workplane("XY")
    .workplane(offset=19)
    .circle(barrel_id / 2)
    .extrude(barrel_h + 5)
)

cylinder_with_fins = cylinder_with_fins.cut(cylinder_bore)

# --- Cylinder head flange (top) ---
head_flange = (
    cq.Workplane("XY")
    .workplane(offset=19 + barrel_h)
    .circle((barrel_od + 12) / 2)
    .extrude(5)
)

# Bolt holes in head flange
bolt_circle_r = (barrel_od + 8) / 2
head_bolts = cq.Workplane("XY").workplane(offset=19 + barrel_h)
for angle in range(0, 360, 45):
    import math
    x = bolt_circle_r * math.cos(math.radians(angle))
    y = bolt_circle_r * math.sin(math.radians(angle))
    bolt_hole = (
        cq.Workplane("XY")
        .workplane(offset=19 + barrel_h)
        .transformed(offset=(x, y, 0))
        .circle(1.5)
        .extrude(5)
    )
    head_flange = head_flange.cut(bolt_hole)

# --- Intake port (side tube) ---
intake = (
    cq.Workplane("YZ")
    .workplane(offset=0)
    .transformed(offset=(0, 5, 0))
    .circle(10)
    .extrude(28)
)

intake_bore = (
    cq.Workplane("YZ")
    .workplane(offset=0)
    .transformed(offset=(0, 5, 0))
    .circle(7)
    .extrude(28)
)

intake_tube = intake.cut(intake_bore)

# --- Exhaust/carburetor stub (front, smaller) ---
carb = (
    cq.Workplane("XZ")
    .workplane(offset=22)
    .transformed(offset=(0, 5, 0))
    .circle(7)
    .extrude(18)
)

carb_bore = (
    cq.Workplane("XZ")
    .workplane(offset=22)
    .transformed(offset=(0, 5, 0))
    .circle(5)
    .extrude(18)
)

carb_tube = carb.cut(carb_bore)

# --- Assembly ---
result = (
    crankcase
    .union(cylinder_with_fins)
    .union(head_flange)
    .union(intake_tube)
    .union(carb_tube)
)

# Final hollow of crankcase
crank_hollow = (
    cq.Workplane("XY")
    .circle(18)
    .extrude(17)
)

result = result.cut(crank_hollow)