import cadquery as cq

# Parameters
gear_box_diam = 40
shell_thickness = 3
body_height = 20
cap_height = 10
total_height = body_height + cap_height
boss_diam = 6
boss_height = 4
screw_diam = 3
n_boss = 3

# Build one half of the shell
shell_outer = cq.Workplane("XY") \
    .circle(gear_box_diam/2 + shell_thickness) \
    .extrude(total_height)

shell_outer = shell_outer.faces(">Z") \
    .workplane() \
    .circle(gear_box_diam/2 + shell_thickness) \
    .extrude(cap_height)

# Hollow out the shell
cavity = cq.Workplane("XY") \
    .circle(gear_box_diam/2) \
    .extrude(total_height + 1)
shell = shell_outer.cut(cavity)

# Add screw bosses
boss = cq.Workplane("XY") \
    .circle(boss_diam/2) \
    .extrude(boss_height) \
    .faces(">Z") \
    .workplane() \
    .hole(screw_diam)

bosses = None
for i in range(n_boss):
    angle = 360/n_boss * i
    b = boss.rotate((0,0,0),(0,0,1),angle) \
            .translate((gear_box_diam/4, 0, body_height/2))
    bosses = b if bosses is None else bosses.union(b)

shell = shell.union(bosses)

# Mirror for the other half
other_half = shell.mirror("XY", (0,0,0))

# Placeholder gears inside
gear1 = cq.Workplane("XY") \
    .circle(15) \
    .extrude(5) \
    .translate((0, 0, body_height/2))

gear2 = cq.Workplane("XY") \
    .circle(10) \
    .extrude(5) \
    .translate((10, 0, body_height/2))

# Final assembly
result = shell.union(other_half).union(gear1).union(gear2)