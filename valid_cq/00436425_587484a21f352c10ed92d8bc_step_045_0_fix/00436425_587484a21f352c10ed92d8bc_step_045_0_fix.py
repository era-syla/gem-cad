import cadquery as cq
import math

shaft_d = 4
head_d = 8
head_thickness = 2
body_length = 30
tip_length = 10

taper_angle = math.degrees(math.atan((shaft_d/2)/tip_length))
slot_depth = 1.5
slot_length = head_d * 0.6
slot_width = 1.5

result = (
    cq.Workplane("XY")
    .circle(head_d/2).extrude(head_thickness)
    .faces("<Z").workplane()
    .circle(shaft_d/2).extrude(body_length)
    .faces("<Z").workplane()
    .circle(shaft_d/2).extrude(tip_length, taper=taper_angle)
)

result = (
    result
    .faces(">Z").workplane()
    .rect(slot_length, slot_width).cutBlind(-slot_depth)
)

result = (
    result
    .faces(">Z").workplane().transformed(rotate=(0, 0, 90))
    .rect(slot_length, slot_width).cutBlind(-slot_depth)
)