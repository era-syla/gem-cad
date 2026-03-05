import cadquery as cq

# Parameters
bed_length = 200
bed_width = 80
bed_height = 10

slot_width = 6
slot_depth = 4
slot_positions = [-bed_width/4, bed_width/4]

# Base bed
result = cq.Workplane("XY").box(bed_length, bed_width, bed_height)

# Cut slots
for y in slot_positions:
    result = (
        result
        .faces(">Z")
        .workplane(origin=(0, y, 0))
        .rect(bed_length, slot_width)
        .cutBlind(-slot_depth)
    )

# Crossbar at end of bed
bar1_thickness = 10
bar1_height = 10
bar1 = (
    cq.Workplane("XY")
    .transformed(offset=(bed_length/2 + bar1_thickness/2, 0, bed_height/2 + bar1_height/2))
    .box(bar1_thickness, bed_width + 2*bar1_thickness, bar1_height)
)

# Handle on top of crossbar
bar2_length = 80
bar2_thickness_y = 10
bar2_height = 10
bar2 = (
    cq.Workplane("XY")
    .transformed(offset=(bed_length/2 + bar1_thickness + bar2_length/2, 0,
                         bed_height + bar1_height/2 + bar2_height/2))
    .box(bar2_length, bar2_thickness_y, bar2_height)
)

# Combine all parts
result = result.union(bar1).union(bar2)