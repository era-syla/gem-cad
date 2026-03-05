import cadquery as cq

# Parameters
width = 20
height = 20
length = 200
slot_width = 4

result = (
    cq.Workplane("XY")
      .box(width, height, length)
      .cut(cq.Workplane("XY").box(width, slot_width, length))
      .cut(cq.Workplane("XY").box(slot_width, height, length))
)