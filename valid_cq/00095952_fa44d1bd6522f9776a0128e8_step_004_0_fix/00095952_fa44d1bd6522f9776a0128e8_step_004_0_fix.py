import cadquery as cq

# Parameters
thickness = 5
outer_r = 30
inner_r = 25
bar_width = 8
bar_length = 20
boss_radius = 4
hole_d = 3

# Base ring
ring = cq.Workplane("XY") \
    .circle(outer_r) \
    .circle(inner_r) \
    .extrude(thickness)

# Offsets
bar_offset = outer_r + bar_width/2
side_boss_offset = outer_r + boss_radius
bottom_boss_offset = bar_offset + bar_length/2

# Top rectangular bar
top_bar = cq.Workplane("XY") \
    .center(0, bar_offset) \
    .rect(bar_length, bar_width) \
    .extrude(thickness)

# Bottom rectangular bar
bottom_bar = cq.Workplane("XY") \
    .center(0, -bar_offset) \
    .rect(bar_width, bar_length) \
    .extrude(thickness)

# Boss creation helper
def boss_at(x, y):
    return cq.Workplane("XY") \
        .center(x, y) \
        .circle(boss_radius) \
        .extrude(thickness)

# Side bosses
boss_left = boss_at(-side_boss_offset, 0)
boss_right = boss_at(side_boss_offset, 0)

# Top bosses at ends of top bar
top_boss_left = boss_at(-bar_length/2, bar_offset)
top_boss_right = boss_at(bar_length/2, bar_offset)

# Bottom boss under bottom bar
bottom_boss = boss_at(0, -bottom_boss_offset)

# Combine all solids
result = ring \
    .union(top_bar) \
    .union(bottom_bar) \
    .union(boss_left) \
    .union(boss_right) \
    .union(top_boss_left) \
    .union(top_boss_right) \
    .union(bottom_boss)

# Create holes through all bosses
hole_points = [
    (-side_boss_offset, 0),
    (side_boss_offset, 0),
    (-bar_length/2, bar_offset),
    (bar_length/2, bar_offset),
    (0, -bottom_boss_offset)
]
result = result.faces(">Z") \
    .workplane() \
    .pushPoints(hole_points) \
    .hole(hole_d, thickness)