import cadquery as cq

# Parameters
head_dia = 20        # diameter across flats for hex head
head_thickness = 8
washer_dia = 24
washer_thickness = 2
shaft_dia = 10
shaft_length = 40
nut_dia = 18         # diameter across flats for nut
nut_thickness = 6
end_cap_thickness = 3

result = (
    cq.Workplane("XY")
    # Bottom hex head
    .polygon(6, head_dia).extrude(head_thickness)
    # Washer on top of head
    .faces(">Z").workplane().circle(washer_dia/2).extrude(washer_thickness)
    # Shaft
    .faces(">Z").workplane().circle(shaft_dia/2).extrude(shaft_length)
    # Mid nut
    .faces(">Z").workplane().polygon(6, nut_dia).extrude(nut_thickness)
    # Threaded portion (simplified as cylinder)
    .faces(">Z").workplane().circle(shaft_dia/2).extrude(shaft_length * 0.3)
    # Bolt end cap
    .faces(">Z").workplane().circle(shaft_dia/2).extrude(end_cap_thickness)
)

result