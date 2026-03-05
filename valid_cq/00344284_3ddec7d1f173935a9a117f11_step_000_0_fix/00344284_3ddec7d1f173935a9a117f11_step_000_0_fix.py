import cadquery as cq

# Parameters
base_length = 100.0
base_width = 20.0
base_thickness = 4.0

block_length = 30.0
block_width = 10.0
block_height = 12.0

hole_diameter = 5.0
hole_offset = 10.0

boss_diameter = 4.0
boss_height = 6.0
boss_offset = 12.0

# Build base plate
result = cq.Workplane("XY").box(base_length, base_width, base_thickness)

# Add center block
result = result.faces(">Z") \
    .workplane() \
    .rect(block_length, block_width) \
    .extrude(block_height)

# Drill holes through the block
result = result.faces(">Y") \
    .workplane() \
    .pushPoints([(-hole_offset, 0), (hole_offset, 0)]) \
    .hole(hole_diameter, block_width + 1)

# Add end bosses on the top face of the base
result = result.faces(">Z") \
    .workplane() \
    .pushPoints([
        ( base_length/2 - boss_offset, 0),
        (-base_length/2 + boss_offset, 0)
    ]) \
    .circle(boss_diameter / 2) \
    .extrude(boss_height)