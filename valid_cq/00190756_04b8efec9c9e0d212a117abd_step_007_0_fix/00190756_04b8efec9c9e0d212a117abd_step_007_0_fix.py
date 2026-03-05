import cadquery as cq

body_radius = 15
body_length = 40
cap_radius = 16
cap_thickness = 5
shaft_radius = 2
shaft_length = 10
boss_radius = 6
boss_thickness = 3
post_radius = 1.5
post_height = 3
post_positions = [(13, 3), (13, -3)]

result = (
    cq.Workplane("XY")
    # Main cylindrical body
    .circle(body_radius).extrude(body_length)
    # Rear end cap
    .faces(">Z").circle(cap_radius).extrude(cap_thickness)
    # Shaft
    .faces(">Z").circle(shaft_radius).extrude(shaft_length)
    # Front boss
    .faces("<Z").workplane().circle(boss_radius).extrude(boss_thickness)
    # Two small front posts
    .faces("<Z").workplane()
    .pushPoints(post_positions).circle(post_radius).extrude(post_height)
)