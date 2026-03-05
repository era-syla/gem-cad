import cadquery as cq

# Parameters
r_big_outer = 20
r_big_inner = 16
th_big = 10
r_small_outer = 8
r_small_inner = 6
th_small = 8
center_distance = 80
beam_width = 6
beam_thickness = 6

# Big end ring
big_ring = (
    cq.Workplane("ZX")
    .circle(r_big_outer)
    .circle(r_big_inner)
    .extrude(beam_thickness)
)

# Small end ring
small_ring = (
    cq.Workplane("ZX")
    .workplane(offset=center_distance)
    .circle(r_small_outer)
    .circle(r_small_inner)
    .extrude(beam_thickness)
)

# Connecting beam
z_bottom = th_big / 2
z_top = center_distance + th_small / 2
beam_height = z_top - z_bottom
beam_center = (z_bottom + z_top) / 2

beam = (
    cq.Workplane("XZ")
    .transformed(offset=(0, 0, beam_center))
    .rect(beam_width, beam_height)
    .extrude(beam_thickness)
)

# Combine all parts
result = big_ring.union(small_ring).union(beam)