import cadquery as cq

R = 15
sep = 40
wall_th = 2
base_th = 2
wall_h = 10
inner_R = R - wall_th
total_h = base_th + wall_h

# Outer shell: two cylinders unioned
outer1 = cq.Workplane("XY").circle(R).extrude(total_h)
outer2 = cq.Workplane("XY").circle(R).extrude(total_h).translate((sep, 0, 0))
bin_outer = outer1.union(outer2)

# Inner void: two smaller cylinders for the cavity
inner1 = cq.Workplane("XY").circle(inner_R).extrude(wall_h).translate((0, 0, base_th))
inner2 = cq.Workplane("XY").circle(inner_R).extrude(wall_h).translate((sep, 0, base_th))
inner_void = inner1.union(inner2)

# Subtract cavity from outer shell to form walls and floor
bin_body = bin_outer.cut(inner_void)

# Create zigzag partitions in the connecting channel
channel_len = sep - 2 * inner_R
N = 6
spacing = channel_len / (N + 1)
partition_thk = 1.5
plate_length = 2 * inner_R

result = bin_body
for i in range(1, N + 1):
    x = -channel_len / 2 + i * spacing
    partition = (
        cq.Workplane("XY")
        .rect(partition_thk, plate_length)
        .extrude(wall_h)
        .translate((x, 0, base_th))
    )
    result = result.cut(partition)