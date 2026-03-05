import cadquery as cq

segment_count = 20
segment_length = 10.0
bar_width = 8.0
bar_thickness = 5.0
hole_diameter = 4.0

length = segment_count * segment_length

result = (
    cq.Workplane("XY")
      .box(length, bar_width, bar_thickness)
      .faces(">Z")
      .workplane()
      .pushPoints([
          (-length/2 + segment_length/2 + i * segment_length, 0)
          for i in range(segment_count)
      ])
      .hole(hole_diameter)
)