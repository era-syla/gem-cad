import cadquery as cq

# Parameters
big_o = 20   # big end outer radius
big_i = 12   # big end inner radius
small_o = 10 # small end outer radius
small_i = 5  # small end inner radius
thickness = 6
length = 60  # center-to-center distance

# Big end ring
big = (
    cq.Workplane("XY")
    .circle(big_o)
    .circle(big_i)
    .extrude(thickness)
)

# Small end ring
small = (
    cq.Workplane("XY")
    .transformed(offset=(length, 0, 0))
    .circle(small_o)
    .circle(small_i)
    .extrude(thickness)
)

# Connecting bar
bar_height = small_o * 2
bar = (
    cq.Workplane("XY")
    .rect(length, bar_height)
    .extrude(thickness)
)

# Combine parts
result = big.union(bar).union(small)

# Slot cut in the bar
slot_length = length - 2 * small_o
slot_width = 6
slot = (
    cq.Workplane("XY")
    .rect(slot_length, slot_width)
    .extrude(thickness + 2)
    .translate((length / 2, 0, 0))
)

result = result.cut(slot)