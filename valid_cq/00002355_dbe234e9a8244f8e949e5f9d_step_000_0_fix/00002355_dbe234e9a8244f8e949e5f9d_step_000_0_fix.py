import cadquery as cq
import math

# Parameters
base_dia = 80
base_thk = 8
num_teeth = 40
tooth_depth = 4
# approximate tooth arc length for width
tooth_width = 2 * math.pi * (base_dia/2) / num_teeth * 0.6
radial_pos = base_dia/2 - tooth_depth/2

boss_dia = 25
boss_thk = 25

ring_count = 3
ring_radial = 1.5
ring_width = 4
ring_gap = 1

slot_width = 2
slot_len = base_dia * 1.2
slot_height = base_thk + boss_thk + ring_count*(ring_width+ring_gap) + 2

# Create base plate
base = cq.Workplane("XY").circle(base_dia/2).extrude(base_thk)

# Create one tooth
tooth = (
    cq.Workplane("XY")
    .transformed(offset=(radial_pos, 0, 0))
    .rect(tooth_depth, tooth_width)
    .extrude(base_thk)
)

# Array teeth around
model = base
for i in range(num_teeth):
    model = model.union(tooth.rotate((0,0,0),(0,0,1), i * 360/num_teeth))

# Create central boss
boss = (
    cq.Workplane("XY", origin=(0, 0, base_thk))
    .circle(boss_dia/2)
    .extrude(boss_thk)
)
model = model.union(boss)

# Create external rings on boss
for i in range(ring_count):
    z0 = base_thk + i*(ring_width + ring_gap)
    ring = (
        cq.Workplane("XY", origin=(0, 0, z0))
        .circle(boss_dia/2 + ring_radial)
        .circle(boss_dia/2)
        .extrude(ring_width)
    )
    model = model.union(ring)

# Cut a radial slot through entire part
slot = (
    cq.Workplane("XY")
    .rect(slot_len, slot_width)
    .extrude(slot_height)
)
model = model.cut(slot)

result = model