import cadquery as cq

# Main body dimensions (NEMA 17 stepper motor style)
body_size = 42.0
body_height = 40.0
corner_radius = 2.0
shaft_diameter = 5.0
shaft_height = 22.0
flange_diameter = 22.0
flange_height = 2.0
mount_hole_diameter = 3.0
mount_hole_offset = 31.0 / 2.0  # from center

# Create main body
body = (
    cq.Workplane("XY")
    .box(body_size, body_size, body_height)
)

# Add rounded corners on the body (vertical edges)
body = body.edges("|Z").fillet(corner_radius)

# Add horizontal groove lines on sides (cosmetic step grooves)
# Groove 1 - lower
groove_depth = 1.0
groove_height = 1.5

body = (
    body
    .faces(">X")
    .workplane()
    .center(0, -body_height/2 + 10)
    .rect(body_size, groove_height)
    .cutBlind(-groove_depth)
)

body = (
    body
    .faces(">X")
    .workplane()
    .center(0, -body_height/2 + 20)
    .rect(body_size, groove_height)
    .cutBlind(-groove_depth)
)

body = (
    body
    .faces("<X")
    .workplane()
    .center(0, -body_height/2 + 10)
    .rect(body_size, groove_height)
    .cutBlind(-groove_depth)
)

body = (
    body
    .faces("<X")
    .workplane()
    .center(0, -body_height/2 + 20)
    .rect(body_size, groove_height)
    .cutBlind(-groove_depth)
)

body = (
    body
    .faces(">Y")
    .workplane()
    .center(0, -body_height/2 + 10)
    .rect(body_size, groove_height)
    .cutBlind(-groove_depth)
)

body = (
    body
    .faces(">Y")
    .workplane()
    .center(0, -body_height/2 + 20)
    .rect(body_size, groove_height)
    .cutBlind(-groove_depth)
)

body = (
    body
    .faces("<Y")
    .workplane()
    .center(0, -body_height/2 + 10)
    .rect(body_size, groove_height)
    .cutBlind(-groove_depth)
)

body = (
    body
    .faces("<Y")
    .workplane()
    .center(0, -body_height/2 + 20)
    .rect(body_size, groove_height)
    .cutBlind(-groove_depth)
)

# Add top flange/boss (circular raised area)
flange = (
    cq.Workplane("XY")
    .workplane(offset=body_height / 2)
    .circle(flange_diameter / 2)
    .extrude(flange_height)
)

body = body.union(flange)

# Add shaft
shaft = (
    cq.Workplane("XY")
    .workplane(offset=body_height / 2 + flange_height)
    .circle(shaft_diameter / 2)
    .extrude(shaft_height)
)

body = body.union(shaft)

# Add mounting holes on top face
body = (
    body
    .faces(">Z")
    .workplane()
    .pushPoints([
        (mount_hole_offset, mount_hole_offset),
        (-mount_hole_offset, mount_hole_offset),
        (mount_hole_offset, -mount_hole_offset),
        (-mount_hole_offset, -mount_hole_offset),
    ])
    .circle(mount_hole_diameter / 2)
    .cutThruAll()
)

result = body