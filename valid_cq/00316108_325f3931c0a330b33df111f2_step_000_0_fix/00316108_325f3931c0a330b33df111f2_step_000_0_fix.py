import cadquery as cq

thickness = 8
width = 20
length_long = 120
length_vert = 70
slot_length = 80
slot_width = 10
hole1_offset = 20
hole2_offset = 50
hole1_d = 10
hole2_d = 6

result = (
    cq.Workplane("XY")
      .polyline([
          (0, 0),
          (length_long, 0),
          (length_long, width),
          (width, width),
          (width, length_vert),
          (0, length_vert),
      ])
      .close()
      .extrude(thickness)
      .faces(">Z").workplane()
        .center(length_long/2, width/2)
        .rect(slot_length, slot_width)
        .cutThruAll()
      .faces(">Z").workplane()
        .center(width/2, width + hole1_offset)
        .circle(hole1_d/2)
        .center(0, hole2_offset - hole1_offset)
        .circle(hole2_d/2)
        .cutThruAll()
)