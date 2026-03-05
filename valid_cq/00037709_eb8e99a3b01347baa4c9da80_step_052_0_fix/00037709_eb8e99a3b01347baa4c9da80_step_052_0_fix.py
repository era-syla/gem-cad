import cadquery as cq

shaft_diameter = 5
shaft_length = 20
head_diameter = 10
head_height = 5
hex_diameter = 4

thread_diameter = 5
thread_length = 10
thread_pitch = 1.25

shaft = cq.Workplane("XY").circle(shaft_diameter / 2).extrude(shaft_length)
head = cq.Workplane("XY").circle(head_diameter / 2).extrude(head_height)

hex_hole = cq.Workplane("XY").polygon(6, hex_diameter).extrude(head_height)

thread = (
    cq.Workplane("XY")
    .circle(thread_diameter / 2)
    .moveTo(0, thread_length)
    .circle(thread_diameter / 2)
    .loft(combine=True)
    .cut(
        cq.Workplane("XZ")
        .workplane(offset=shaft_length - thread_pitch / 2)
        .polygon(3, thread_diameter / 2)
        .extrude(-thread_pitch)
    )
    .rotate((0, 0, 0), (0, 1, 0), 360 / (thread_length / thread_pitch))
)

result = shaft.union(head).cut(hex_hole).cut(thread)