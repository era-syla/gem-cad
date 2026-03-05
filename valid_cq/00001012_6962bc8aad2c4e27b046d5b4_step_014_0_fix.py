import cadquery as cq

# Main body dimensions
body_w = 60
body_h = 50
body_d = 50

# Create main rectangular body
body = cq.Workplane("XY").box(body_w, body_d, body_h)

# Cut the large cylindrical hole through the top (vertical axis)
cylinder_r = 18
body = body.faces(">Z").workplane().circle(cylinder_r).cutThruAll()

# Cut slots on left and right sides (the vertical slots visible on front/back faces)
slot_w = 8
slot_h = body_h * 0.6
slot_d = body_d

# Left slot cut
body = (body
    .faces(">X").workplane(centerOption="CenterOfBoundBox")
    .center(0, 5)
    .rect(slot_d, slot_h)
    .cutBlind(-slot_w)
)

# Right slot cut
body = (body
    .faces("<X").workplane(centerOption="CenterOfBoundBox")
    .center(0, 5)
    .rect(slot_d, slot_h)
    .cutBlind(-slot_w)
)

# Add mounting flanges on left and right (wider tabs at top)
flange_w = 10
flange_h = 12
flange_d = body_d

body = (body
    .faces(">X").workplane(centerOption="CenterOfBoundBox")
    .center(0, body_h/2 - flange_h/2)
    .rect(flange_d, flange_h)
    .extrude(flange_w)
)

body = (body
    .faces("<X").workplane(centerOption="CenterOfBoundBox")
    .center(0, body_h/2 - flange_h/2)
    .rect(flange_d, flange_h)
    .extrude(flange_w)
)

# Add bolt holes on front face (3 holes in a column)
hole_r = 3
hole_spacing = 12
hole_x_offset = 20

# Front face holes - right side column
body = (body
    .faces(">Y").workplane(centerOption="CenterOfBoundBox")
    .pushPoints([
        (hole_x_offset, -hole_spacing),
        (hole_x_offset, 0),
        (hole_x_offset, hole_spacing),
    ])
    .circle(hole_r)
    .cutThruAll()
)

# Front face holes - left side column
body = (body
    .faces(">Y").workplane(centerOption="CenterOfBoundBox")
    .pushPoints([
        (-hole_x_offset, -hole_spacing),
        (-hole_x_offset, 0),
        (-hole_x_offset, hole_spacing),
    ])
    .circle(hole_r)
    .cutThruAll()
)

# Add small notch at top of cylinder opening
notch_w = 10
notch_d = 8
notch_h = 12

body = (body
    .faces(">Z").workplane(centerOption="CenterOfBoundBox")
    .rect(notch_w, notch_d)
    .cutBlind(notch_h)
)

result = body