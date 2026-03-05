import cadquery as cq

# Parameters
r_inner = 25
r_outer = 27
ring_height = 6
block_depth = 8
block_height = 4
block_thickness = 6
hole_dia = 4

# Base ring
result = cq.Workplane("XY") \
    .circle(r_outer) \
    .circle(r_inner) \
    .extrude(ring_height)

# Top lug block
top_block = cq.Workplane("YZ", origin=(0, r_outer, ring_height/2 + block_height/2)) \
    .rect(block_depth, block_height) \
    .extrude(block_thickness)

# Bottom lug block
bottom_block = cq.Workplane("YZ", origin=(0, r_outer, -ring_height/2 - block_height/2)) \
    .rect(block_depth, block_height) \
    .extrude(block_thickness)

# Drill holes through lugs
hole_cutter_top = cq.Workplane("YZ", origin=(block_thickness/2, r_outer, ring_height/2 + block_height/2)) \
    .circle(hole_dia/2) \
    .extrude(block_thickness)
hole_cutter_bottom = cq.Workplane("YZ", origin=(block_thickness/2, r_outer, -ring_height/2 - block_height/2)) \
    .circle(hole_dia/2) \
    .extrude(block_thickness)

# Combine all and subtract holes
result = result.union(top_block).union(bottom_block) \
    .cut(hole_cutter_top) \
    .cut(hole_cutter_bottom)
