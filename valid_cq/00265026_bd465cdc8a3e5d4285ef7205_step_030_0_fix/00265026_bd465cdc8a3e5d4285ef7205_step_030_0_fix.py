import cadquery as cq

# Parameters
plate_length_total = 100.0
plate_width = 40.0
plate_thickness = 5.0
gap = 5.0

peg_length = 10.0
post_width = 4.0
post_height = 4.0
post_separation = 10.0
bar_width = 4.0
bar_height = post_separation - post_height

half_length = plate_length_total / 2.0
left_center_x = -(half_length / 2.0 + gap / 2.0)
right_center_x =  (half_length / 2.0 + gap / 2.0)

# Left plate with male connector
left = (
    cq.Workplane("XY")
    .transformed(offset=(left_center_x, 0, 0))
    .box(half_length, plate_width, plate_thickness)
    .faces(">X").workplane()
    .pushPoints([(0, post_separation/2.0), (0, -post_separation/2.0)])
    .rect(post_width, post_height).extrude(peg_length)
    .rect(bar_width, bar_height).extrude(peg_length)
)

# Right plate with female pocket
right = (
    cq.Workplane("XY")
    .transformed(offset=(right_center_x, 0, 0))
    .box(half_length, plate_width, plate_thickness)
    .faces("<X").workplane()
    .pushPoints([(0, post_separation/2.0), (0, -post_separation/2.0)])
    .rect(post_width, post_height).cutBlind(peg_length)
    .rect(bar_width, bar_height).cutBlind(peg_length)
)

result = left.union(right)