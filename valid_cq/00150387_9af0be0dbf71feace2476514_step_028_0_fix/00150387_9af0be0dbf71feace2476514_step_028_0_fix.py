import cadquery as cq

# Dimensions
bottom_r = 8
bottom_h = 8
groove_outer_r = 11
groove_inner_r = 9
groove_depth = 2
mid_r = 10
mid_h = 30
thread_pitch = 2
thread_depth = 1
block_size = 20
block_h = 10
nut_diameter = 10
nut_h = 5

# Build bottom cylinder
result = cq.Workplane("XY").circle(bottom_r).extrude(bottom_h)

# Base groove
result = result.faces(">Z").workplane().circle(groove_outer_r).circle(groove_inner_r).extrude(-groove_depth)

# Main cylinder
result = result.faces(">Z").workplane().circle(mid_r).extrude(mid_h)

# Approximate threads with ring cuts
nRings = int(mid_h / thread_pitch)
for i in range(nRings):
    offset = i * thread_pitch - mid_h
    result = result.faces(">Z").workplane(offset=offset).circle(mid_r).circle(mid_r - thread_depth).extrude(-thread_depth)

# Top square block
result = result.faces(">Z").workplane().rect(block_size, block_size).extrude(block_h)

# Hexagonal nut on top
result = result.faces(">Z").workplane().polygon(6, nut_diameter).extrude(nut_h)