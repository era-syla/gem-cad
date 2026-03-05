import cadquery as cq

# Parameters
pin_d = 4
gap = pin_d + 2
tine_thk = 5
tine_w = 12
tine_len = 6
stem_d = 10
stem_len = 10
body_d = 20
body_len = 60
collar_thk = 2
collar_d = body_d + 2

# Compute key X positions
base1 = tine_len + stem_len
base2 = base1 + body_len + collar_thk
base3 = base2 + stem_len

# Front clevis tines
front_tine1 = (
    cq.Workplane("YZ")
    .transformed(offset=(0, 0, gap/2 + tine_thk/2))
    .rect(tine_w, tine_thk)
    .extrude(tine_len)
)
front_tine2 = (
    cq.Workplane("YZ")
    .transformed(offset=(0, 0, -(gap/2 + tine_thk/2)))
    .rect(tine_w, tine_thk)
    .extrude(tine_len)
)
# Front pin
front_pin = (
    cq.Workplane("XZ")
    .transformed(offset=(tine_len/2, -(tine_w + 2)/2, 0))
    .circle(pin_d/2)
    .extrude(tine_w + 2)
)

# First stem
stem1 = (
    cq.Workplane("YZ")
    .transformed(offset=(tine_len, 0, 0))
    .circle(stem_d/2)
    .extrude(stem_len)
)

# Body cylinder
body = (
    cq.Workplane("YZ")
    .transformed(offset=(base1, 0, 0))
    .circle(body_d/2)
    .extrude(body_len)
)

# Collar on body
collar = (
    cq.Workplane("YZ")
    .transformed(offset=(base1 + collar_thk/2, 0, 0))
    .circle(collar_d/2)
    .extrude(collar_thk)
)

# Second stem
stem2 = (
    cq.Workplane("YZ")
    .transformed(offset=(base2, 0, 0))
    .circle(stem_d/2)
    .extrude(stem_len)
)

# Rear clevis tines
rear_tine1 = (
    cq.Workplane("YZ")
    .transformed(offset=(base2 + tine_len, 0, gap/2 + tine_thk/2))
    .rect(tine_w, tine_thk)
    .extrude(tine_len)
)
rear_tine2 = (
    cq.Workplane("YZ")
    .transformed(offset=(base2 + tine_len, 0, -(gap/2 + tine_thk/2)))
    .rect(tine_w, tine_thk)
    .extrude(tine_len)
)
# Rear pin
rear_pin = (
    cq.Workplane("XZ")
    .transformed(offset=(base2 + tine_len + tine_len/2, -(tine_w + 2)/2, 0))
    .circle(pin_d/2)
    .extrude(tine_w + 2)
)

# Assemble all parts
result = (
    front_tine1
    .union(front_tine2)
    .union(front_pin)
    .union(stem1)
    .union(body)
    .union(collar)
    .union(stem2)
    .union(rear_tine1)
    .union(rear_tine2)
    .union(rear_pin)
)