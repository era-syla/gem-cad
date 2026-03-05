import cadquery as cq

# Main vertical tube (rod holder)
tube_outer_r = 15
tube_inner_r = 12
tube_height = 100

# Base/collar at bottom
base_outer_r = 20
base_height = 20

# Clamp ring parameters
clamp_r = 18
clamp_tube_r = 12
clamp_thickness = 6
clamp_offset_x = 35
clamp_z = 10

# Build main tube
main_tube = (
    cq.Workplane("XY")
    .circle(tube_outer_r)
    .extrude(tube_height)
)

# Hollow out main tube
main_tube = (
    main_tube
    .faces(">Z")
    .workplane()
    .circle(tube_inner_r)
    .cutBlind(-tube_height)
)

# Build tapered base
base = (
    cq.Workplane("XY")
    .circle(base_outer_r)
    .workplane(offset=base_height)
    .circle(tube_outer_r)
    .loft()
)

# Combine tube and base
result = main_tube.union(base)

# Add clamp ring body - a torus-like ring
clamp_ring = (
    cq.Workplane("XZ")
    .transformed(offset=cq.Vector(clamp_offset_x, clamp_z, 0))
    .circle(clamp_r + clamp_thickness)
    .extrude(clamp_thickness)
)

clamp_ring_inner = (
    cq.Workplane("XZ")
    .transformed(offset=cq.Vector(clamp_offset_x, clamp_z, 0))
    .circle(clamp_r)
    .extrude(clamp_thickness)
)

clamp_ring = clamp_ring.cut(clamp_ring_inner)

# Add connecting arm from main tube to clamp ring
arm = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(tube_outer_r, 0, clamp_z))
    .rect(clamp_offset_x - tube_outer_r, clamp_thickness * 2)
    .extrude(clamp_thickness)
)

result = result.union(clamp_ring).union(arm)

# Add bolt lug at top of clamp
bolt_lug_top = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(clamp_offset_x, -(clamp_r + clamp_thickness), clamp_z + clamp_thickness + 2))
    .rect(10, 8)
    .extrude(8)
)

bolt_lug_bot = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(clamp_offset_x, -(clamp_r + clamp_thickness), clamp_z - 8))
    .rect(10, 8)
    .extrude(8)
)

result = result.union(bolt_lug_top).union(bolt_lug_bot)

# Add small bolt holes through lugs
bolt_hole_top = (
    cq.Workplane("YZ")
    .transformed(offset=cq.Vector(-(clamp_r + clamp_thickness + 4), clamp_z + clamp_thickness + 6, clamp_offset_x))
    .circle(2)
    .extrude(16)
)

bolt_hole_bot = (
    cq.Workplane("YZ")
    .transformed(offset=cq.Vector(-(clamp_r + clamp_thickness + 4), clamp_z - 4, clamp_offset_x))
    .circle(2)
    .extrude(16)
)

result = result.cut(bolt_hole_top).cut(bolt_hole_bot)

# Cut slot in clamp ring to allow clamping
slot = (
    cq.Workplane("XZ")
    .transformed(offset=cq.Vector(clamp_offset_x, clamp_z - 1, 0))
    .rect(2, clamp_thickness + 2)
    .extrude(clamp_r * 2 + clamp_thickness * 2 + 2)
    .translate(cq.Vector(0, -(clamp_r + clamp_thickness + 1), 0))
)

# Simple slot cut through bottom of ring
slot2 = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(clamp_offset_x, -(clamp_r + 2), clamp_z - 1))
    .rect(2, 8)
    .extrude(clamp_thickness + 2)
)

result = result.cut(slot2)