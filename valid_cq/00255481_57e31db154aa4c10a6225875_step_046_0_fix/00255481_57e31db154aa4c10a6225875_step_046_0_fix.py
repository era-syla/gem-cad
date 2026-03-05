import cadquery as cq

# Parameters
OD = 50.0
wall_t = 3.0
shell_H = 20.0
bot_t = 3.0
hole_d = 8.0
hole_positions = [(15.0, 0.0), (-15.0, 0.0)]
shaft_d = 6.0
shaft_len = 60.0

# Outer shell
outer = cq.Workplane("XY").circle(OD/2).extrude(shell_H)

# Hollow the shell leaving a bottom thickness
inner_cut = cq.Workplane("XY").workplane(offset=bot_t).circle(OD/2 - wall_t).extrude(shell_H - bot_t)
shell = outer.cut(inner_cut)

# Base disc
base = cq.Workplane("XY").circle(OD/2 - wall_t).extrude(bot_t)

# Combine shell and base
part = shell.union(base)

# Cut holes through the base disc
for x, y in hole_positions:
    part = part.cut(
        cq.Workplane("XY")
        .center(x, y)
        .circle(hole_d/2)
        .extrude(bot_t)
    )

# Central shaft
shaft = cq.Workplane("XY").circle(shaft_d/2).extrude(shaft_len, both=True)

# Final result
result = part.union(shaft)