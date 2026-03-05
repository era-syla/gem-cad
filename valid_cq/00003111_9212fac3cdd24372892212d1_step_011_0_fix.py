import cadquery as cq

# Large bearing
large_outer_r = 20
large_inner_r = 8
large_height = 14

# Small bushing
small_outer_r = 8
small_inner_r = 5
small_height = 8

# Create large bearing (outer ring with inner bore and groove details)
large_bearing = (
    cq.Workplane("XY")
    .circle(large_outer_r)
    .circle(large_inner_r)
    .extrude(large_height)
)

# Add chamfers to large bearing edges
large_bearing = (
    large_bearing
    .faces(">Z").edges()
    .chamfer(0.8)
)

large_bearing = (
    large_bearing
    .faces("<Z").edges()
    .chamfer(0.8)
)

# Add inner groove detail on large bearing - cut a groove on the inner face
groove_depth = 1.5
groove_width = large_height * 0.6

large_bearing = (
    large_bearing
    .workplane(offset=large_height / 2)
    .transformed(offset=(0, 0, 0))
    .circle(large_inner_r + groove_depth)
    .circle(large_inner_r)
    .cutBlind(-groove_width, clean=False)
)

# Add outer lip/shield detail - recessed rings on outer face
shield_depth = 1.0
shield_offset = 2.0

large_bearing = (
    large_bearing
    .faces(">Z")
    .workplane()
    .circle(large_outer_r - 0.1)
    .circle(large_outer_r - shield_offset)
    .cutBlind(-shield_depth)
)

large_bearing = (
    large_bearing
    .faces("<Z")
    .workplane()
    .circle(large_outer_r - 0.1)
    .circle(large_outer_r - shield_offset)
    .cutBlind(-shield_depth)
)

# Create small bushing
small_bushing = (
    cq.Workplane("XY")
    .transformed(offset=(large_outer_r + small_outer_r + 4, 0, 0))
    .circle(small_outer_r)
    .circle(small_inner_r)
    .extrude(small_height)
)

# Add chamfers to small bushing
small_bushing = (
    small_bushing
    .faces(">Z").edges()
    .chamfer(0.5)
)

small_bushing = (
    small_bushing
    .faces("<Z").edges()
    .chamfer(0.5)
)

# Combine both parts
result = large_bearing.add(small_bushing)