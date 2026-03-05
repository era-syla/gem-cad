import cadquery as cq

# Parameters
base_thickness = 3.0
central_radius = 6.0
arm_length = 20.0
arm_width = 4.0
boss_diameter = 8.0
boss_height = 10.0
hole_diameter = 3.0

# Create central diamond-shaped plate
base = (
    cq.Workplane("XY")
    .polyline([
        (0, central_radius),
        (central_radius, 0),
        (0, -central_radius),
        (-central_radius, 0),
        (0, central_radius),
    ])
    .close()
    .extrude(base_thickness)
)

# Add arms and bosses at 0, 90, 180, 270 degrees
for angle in [0, 90, 180, 270]:
    # Arm
    arm = (
        cq.Workplane("XY")
        .transformed(rotate=(0, 0, angle))
        .rect(arm_length, arm_width, centered=(False, True))
        .extrude(base_thickness)
    )
    base = base.union(arm)
    # Boss outer cylinder
    boss_outer = (
        cq.Workplane("XY")
        .transformed(rotate=(0, 0, angle), offset=(0, 0, base_thickness))
        .center(arm_length, 0)
        .circle(boss_diameter / 2)
        .extrude(boss_height)
    )
    # Boss inner hole cylinder
    boss_hole = (
        cq.Workplane("XY")
        .transformed(rotate=(0, 0, angle), offset=(0, 0, base_thickness))
        .center(arm_length, 0)
        .circle(hole_diameter / 2)
        .extrude(boss_height)
    )
    boss = boss_outer.cut(boss_hole)
    base = base.union(boss)

result = base