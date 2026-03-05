import cadquery as cq

# Parameters
block_len = 40
block_w = 20
block_h = 20
transition_len = 30
tube_len = 40
tube_od = 20
wall_thickness = 2
tube_id = tube_od - 2 * wall_thickness

# Rectangular block
block = cq.Workplane("YZ").rect(block_w, block_h).extrude(-block_len)

# Transition loft from rectangle to circle
transition = (
    cq.Workplane("YZ")
    .rect(block_w, block_h)
    .workplane(offset=transition_len)
    .circle(tube_od / 2)
    .loft()
)

# Cylindrical tube
tube = (
    cq.Workplane("YZ")
    .workplane(offset=transition_len)
    .circle(tube_od / 2)
    .extrude(tube_len)
)

# Combine outer geometry
outer = block.union(transition).union(tube)

# Inner cut for hollow tube
inner_cut = (
    cq.Workplane("YZ")
    .workplane(offset=transition_len)
    .circle(tube_id / 2)
    .extrude(tube_len + 1)
)

# Final result
result = outer.cut(inner_cut)