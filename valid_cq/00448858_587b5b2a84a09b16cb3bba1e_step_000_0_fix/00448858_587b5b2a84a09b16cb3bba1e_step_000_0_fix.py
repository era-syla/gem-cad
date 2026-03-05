import cadquery as cq

# Parameters
R_flange = 15
H_flange = 5
R_shank = 10
H_shank = 50
H_head = 8
R_boss = 5
H_boss = 3

# Base flange and shank
base = (
    cq.Workplane("XY")
    .circle(R_flange).extrude(H_flange)
    .circle(R_shank).extrude(H_shank)
)

# Head profile on XZ plane, to be revolved about Y axis
head_profile = [
    (R_shank, 0),
    ((R_shank + R_boss) / 2, H_head * 1.4),
    (R_boss, H_head),
    (0, H_head),
    (0, 0)
]
head = (
    cq.Workplane("XZ")
    .polyline(head_profile).close()
    .revolve(360, axisStart=(0, 0, 0), axisEnd=(0, 1, 0))
    .translate((0, 0, H_flange + H_shank))
)

# Top boss cylinder
boss = (
    cq.Workplane("XY")
    .workplane(offset=H_flange + H_shank + H_head)
    .circle(R_boss).extrude(H_boss)
)

result = base.union(head).union(boss)