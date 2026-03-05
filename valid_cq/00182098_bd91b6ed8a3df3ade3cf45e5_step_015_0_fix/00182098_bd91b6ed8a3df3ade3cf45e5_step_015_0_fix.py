import cadquery as cq

# Dimensions (all in mm)
body_d = 10
body_len = 18
groove_d = 11
groove_depth = 1.5
collar_d = 12
collar_len = 2
nut_ff = 14
nut_thickness = 3
post_d = 8
post_len = 8
button_d = 7
button_len = 10
term_len = 8
term_w = 5
term_t = 1
term_offset = 2.5

# Build the main body (extrude downward)
result = (
    cq.Workplane("XY")
      .circle(body_d/2)
      .extrude(-body_len)
)

# Add the two flat terminals on the back face
result = (
    result.faces("<Z").workplane()
      .center(term_offset, 0).rect(term_w, term_t).extrude(term_len)
      .faces("<Z").workplane()
      .center(-term_offset, 0).rect(term_w, term_t).extrude(term_len)
)

# Add a circumferential groove at the front of the body
result = (
    result.faces(">Z").workplane()
      .circle(groove_d/2)
      .cutBlind(groove_depth)
)

# Add the collar (cylindrical flange)
result = (
    result.faces(">Z").workplane()
      .circle(collar_d/2)
      .extrude(collar_len)
)

# Add the hex nut
result = (
    result.faces(">Z").workplane()
      .polygon(6, nut_ff)
      .extrude(nut_thickness)
)

# Add the post above the nut
result = (
    result.faces(">Z").workplane()
      .circle(post_d/2)
      .extrude(post_len)
)

# Add the button plunger
result = (
    result.faces(">Z").workplane()
      .circle(button_d/2)
      .extrude(button_len)
)