import cadquery as cq

# GoPro-style camera mount adapter
# Building from bottom up

# Base plate - rounded rectangular base
base = (
    cq.Workplane("XY")
    .rect(50, 40)
    .extrude(4)
)

# Round the base corners
base = base.edges("|Z").fillet(6)

# Add slight taper/chamfer to bottom edges
base = base.edges("<Z").chamfer(1)

# Middle body section
body = (
    cq.Workplane("XY")
    .workplane(offset=4)
    .rect(38, 30)
    .extrude(12)
)
body = body.edges("|Z").fillet(4)

# Combine base and body
result = base.union(body)

# Front mounting prongs (two finger mount - GoPro style)
# Left prong
left_prong = (
    cq.Workplane("XY")
    .workplane(offset=4)
    .center(-8, 15)
    .rect(12, 8)
    .extrude(18)
)
left_prong = left_prong.edges("|Z").fillet(3)

# Right prong
right_prong = (
    cq.Workplane("XY")
    .workplane(offset=4)
    .center(8, 15)
    .rect(12, 8)
    .extrude(18)
)
right_prong = right_prong.edges("|Z").fillet(3)

result = result.union(left_prong).union(right_prong)

# Center connector between prongs
center_conn = (
    cq.Workplane("XY")
    .workplane(offset=16)
    .center(0, 15)
    .rect(6, 8)
    .extrude(6)
)
result = result.union(center_conn)

# Bolt hole through prongs (horizontal axis)
bolt_hole = (
    cq.Workplane("YZ")
    .workplane(offset=0)
    .center(15, 13)
    .circle(3)
    .extrude(30)
)
result = result.cut(bolt_hole)

# Threaded knob/bolt cylinder on the side
knob = (
    cq.Workplane("YZ")
    .workplane(offset=-22)
    .center(15, 13)
    .circle(6)
    .extrude(4)
)
result = result.union(knob)

# Knob detail rings
knob2 = (
    cq.Workplane("YZ")
    .workplane(offset=-20)
    .center(15, 13)
    .circle(5)
    .extrude(2)
)
result = result.union(knob2)

# Hex socket in knob
hex_cut = (
    cq.Workplane("YZ")
    .workplane(offset=-22)
    .center(15, 13)
    .polygon(6, 6)
    .extrude(3)
)
result = result.cut(hex_cut)

# Side clip features on base sides
# Left clip
left_clip = (
    cq.Workplane("XZ")
    .workplane(offset=-20)
    .center(2, 2)
    .rect(8, 6)
    .extrude(4)
)
left_clip = left_clip.edges("|Y").fillet(1.5)
result = result.union(left_clip)

# Right clip
right_clip = (
    cq.Workplane("XZ")
    .workplane(offset=20)
    .center(2, 2)
    .rect(8, 6)
    .extrude(4)
)
right_clip = right_clip.edges("|Y").fillet(1.5)
result = result.union(right_clip)

# Slot cut in base front
slot = (
    cq.Workplane("XY")
    .workplane(offset=1)
    .center(0, 12)
    .rect(30, 2)
    .extrude(3)
)
result = result.cut(slot)

# Add ribbed texture to top connector (simplified as cylinders)
rib1 = (
    cq.Workplane("XY")
    .workplane(offset=20)
    .center(0, 15)
    .circle(5.5)
    .extrude(1.5)
)
result = result.union(rib1)

rib2 = (
    cq.Workplane("XY")
    .workplane(offset=22)
    .center(0, 15)
    .circle(5.5)
    .extrude(1.5)
)
result = result.union(rib2)