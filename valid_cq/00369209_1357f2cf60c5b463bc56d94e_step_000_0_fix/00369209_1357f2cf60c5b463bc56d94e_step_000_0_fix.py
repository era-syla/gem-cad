import cadquery as cq
import math

flat2flat = 10
shaft_dia = 5
shaft_len = 30
shoulder_dia = 6
shoulder_len = 2
head_height = 4

hex_dia = flat2flat / math.cos(math.pi/6)

result = (
    cq.Workplane("XY")
      .circle(shaft_dia/2)
      .extrude(shaft_len)
      .faces(">Z")
      .circle(shoulder_dia/2)
      .extrude(shoulder_len)
      .faces(">Z")
      .polygon(6, hex_dia)
      .extrude(head_height)
)