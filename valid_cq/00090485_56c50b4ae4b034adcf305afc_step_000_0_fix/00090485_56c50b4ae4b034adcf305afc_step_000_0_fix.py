import cadquery as cq

# Parameters
prong_length = 20
prong_height = 20
plate_thickness = 5
prong_gap = 10

body_dia = 40
body_len = 100

ring_outer = 44
ring_inner = 40
ring_thick = 6

rod_dia = 20
rod_len = 80

eye_outer = 20
eye_thick = 10
eye_hole = 8

# Create two clevis prongs
prong1 = (
    cq.Workplane("XY")
    .box(prong_length, prong_height, plate_thickness)
    .translate((prong_length/2, prong_gap/2 + prong_height/2, 0))
)
prong2 = (
    cq.Workplane("XY")
    .box(prong_length, prong_height, plate_thickness)
    .translate((prong_length/2, -(prong_gap/2 + prong_height/2), 0))
)

# Create the main cylinder body
body = (
    cq.Workplane("YZ")
    .circle(body_dia/2)
    .extrude(body_len)
    .translate((prong_length, 0, 0))
)

# Combine prongs and body
geom = prong1.union(prong2).union(body)

# Add a ring at the front of the body
geom = (
    geom.faces(">X")
    .workplane()
    .circle(ring_outer/2)
    .circle(ring_inner/2)
    .extrude(ring_thick)
)

# Add the piston rod
geom = (
    geom.faces(">X")
    .workplane()
    .circle(rod_dia/2)
    .extrude(rod_len)
)

# Add the pivot eye at the end of the rod
geom = (
    geom.faces(">X")
    .workplane()
    .circle(eye_outer/2)
    .extrude(eye_thick)
    .faces(">X")
    .workplane()
    .hole(eye_hole)
)

result = geom