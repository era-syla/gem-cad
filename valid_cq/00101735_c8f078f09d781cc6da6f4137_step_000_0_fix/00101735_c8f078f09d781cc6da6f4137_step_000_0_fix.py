import cadquery as cq

# Parameters
overall_length = 200
overall_width = 20
overall_thickness = 8

slot_length = 160
slot_width = 6
slot_depth = 4

big_hole_dia = 5
big_hole_count = 5

small_hole_dia = 3
small_hole_offset = 4  # distance from end of plate

# Compute hole positions (centered on X axis, Y=0)
big_hole_positions = [
    (
        -slot_length/2 + i * (slot_length/(big_hole_count - 1)),
        0
    )
    for i in range(big_hole_count)
]

small_hole_positions = [
    ( overall_length/2 - small_hole_offset, 0),
    (-overall_length/2 + small_hole_offset, 0)
]

# Build the part
result = (
    cq.Workplane("XY")
    # Base plate
    .box(overall_length, overall_width, overall_thickness)
    # Fillet all vertical edges
    .edges("|Z").fillet(1)
    # Create slot pocket on top face
    .faces(">Z").workplane()
      .rect(slot_length, slot_width)
      .cutBlind(-slot_depth)
    # Drill the big holes through the plate
    .faces(">Z").workplane()
      .pushPoints(big_hole_positions)
      .hole(big_hole_dia)
    # Drill the small end holes through the plate
    .faces(">Z").workplane()
      .pushPoints(small_hole_positions)
      .hole(small_hole_dia)
)
