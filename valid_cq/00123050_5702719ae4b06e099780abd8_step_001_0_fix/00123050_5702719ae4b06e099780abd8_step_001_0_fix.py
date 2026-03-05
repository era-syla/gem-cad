import cadquery as cq

# Parameters
barrel_d = 20
barrel_l = 60
collar_d = 25
collar_t = 5
rod_d = 10
rod_l = 50
fork_th = 3
pin_d = 5
fork_gap = pin_d + 2
fork_offset = fork_th/2 + fork_gap/2
prong_depth = rod_d + 2
prong_length = 6
collar_center = barrel_l * 0.2

# Build barrel
barrel = cq.Workplane("XY").circle(barrel_d/2).extrude(barrel_l)

# Build rod
rod = cq.Workplane("XY").circle(rod_d/2).extrude(-rod_l)

# Combine barrel and rod
result = barrel.union(rod)

# Add collar on barrel
result = result.union(
    cq.Workplane("XY")
      .transformed(offset=(0, 0, collar_center - collar_t/2))
      .circle(collar_d/2)
      .extrude(collar_t)
)

# Add clevis prongs and pins at both ends
for end_z, direction in [(-rod_l, -prong_length), (barrel_l, prong_length)]:
    # Prongs
    prong1 = cq.Workplane("XY").transformed(offset=(fork_offset, 0, end_z)).rect(fork_th, prong_depth).extrude(direction)
    prong2 = cq.Workplane("XY").transformed(offset=(-fork_offset, 0, end_z)).rect(fork_th, prong_depth).extrude(direction)
    result = result.union(prong1).union(prong2)
    # Pin holes
    hole_z = end_z + direction/2
    hole_len = prong_depth + 2
    for x_off in (fork_offset, -fork_offset):
        hole = cq.Workplane("XZ", origin=(x_off, 0, hole_z)).circle(pin_d/2).extrude(hole_len, both=True)
        result = result.cut(hole)