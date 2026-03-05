import cadquery as cq

# Dimensions
fw_size = 40
fw_th = 3
hole_positions = [(-15, -15), (15, -15), (15, 15), (-15, 15)]
hole_d = 4
rod_d = 4
rod_len = 40
shaft1_d = 12
shaft1_len = 20
shaft2_d = 10
shaft2_len = 60
disc_d = 40
disc_th = 3
web_th = 2
web_clearance = 2  # radial thickness inside cavity
web_h = shaft1_len

# Flange with mounting holes
flange = (
    cq.Workplane("XY")
    .box(fw_size, fw_size, fw_th)
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_d)
)

# Rod on front side (negative Z)
rod = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .circle(rod_d / 2)
    .extrude(-rod_len)
)

# First cylinder body (houses internal cavity and webs)
cylinder_body = (
    cq.Workplane("XY")
    .workplane(offset=fw_th)
    .circle(shaft1_d / 2)
    .extrude(shaft1_len)
)
# Internal cavity
cavity = (
    cq.Workplane("XY")
    .workplane(offset=fw_th)
    .circle((shaft1_d / 2) - web_clearance)
    .extrude(shaft1_len)
)
cylinder_body = cylinder_body.cut(cavity)

# Second shaft
shaft2 = (
    cq.Workplane("XY")
    .workplane(offset=fw_th + shaft1_len)
    .circle(shaft2_d / 2)
    .extrude(shaft2_len)
)

# Disc on the far end
disc = (
    cq.Workplane("XY")
    .workplane(offset=fw_th + shaft1_len + shaft2_len)
    .circle(disc_d / 2)
    .extrude(disc_th)
)

# Assemble basic parts
result = flange.union(rod).union(cylinder_body).union(shaft2).union(disc)

# Add three radial webs inside the first cylinder section
for angle in [0, 120, 240]:
    web = (
        cq.Workplane("XY")
        .workplane(offset=fw_th)
        .rect(web_th, (shaft1_d - web_clearance * 2))
        .extrude(web_h)
        .rotate((0, 0, 0), (0, 0, 1), angle)
    )
    result = result.union(web)