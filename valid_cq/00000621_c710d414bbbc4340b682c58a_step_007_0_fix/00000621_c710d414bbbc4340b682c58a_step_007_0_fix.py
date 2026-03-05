import cadquery as cq

# T-slot aluminum extrusion profile (20x20mm style, 2-slot top)
# This is a twin-slot rail / linear rail profile

length = 200
w = 20  # width
h = 10  # height

# Create the main rectangular body
profile = (
    cq.Workplane("XY")
    .rect(w * 2, h)
    .extrude(length)
)

# Add the slot channels on top (two T-slots running along length)
slot_width = 6
slot_depth = 3
slot_inner_width = 10
slot_inner_depth = 2

# Left slot
slot1 = (
    cq.Workplane("XY")
    .center(-w / 2, h / 2 - slot_depth)
    .rect(slot_width, slot_depth)
    .extrude(length)
)

# Right slot
slot2 = (
    cq.Workplane("XY")
    .center(w / 2, h / 2 - slot_depth)
    .rect(slot_width, slot_depth)
    .extrude(length)
)

# Center groove between the two slots
center_groove = (
    cq.Workplane("XY")
    .center(0, h / 2 - 1.5)
    .rect(3, 3)
    .extrude(length)
)

result = profile.cut(slot1).cut(slot2).cut(center_groove)

# Add rounded slot details - undercut for T-slot
undercut_w = 9
undercut_d = 1.5

undercut1 = (
    cq.Workplane("XY")
    .center(-w / 2, h / 2 - slot_depth - undercut_d / 2)
    .rect(undercut_w, undercut_d)
    .extrude(length)
)

undercut2 = (
    cq.Workplane("XY")
    .center(w / 2, h / 2 - slot_depth - undercut_d / 2)
    .rect(undercut_w, undercut_d)
    .extrude(length)
)

result = result.cut(undercut1).cut(undercut2)

# Add longitudinal grooves on sides (rails)
groove_h = 2
groove_d = 1

# Left side groove
left_groove = (
    cq.Workplane("XY")
    .center(-w - groove_d / 2, 0)
    .rect(groove_d, groove_h)
    .extrude(length)
)

# Right side groove  
right_groove = (
    cq.Workplane("XY")
    .center(w + groove_d / 2, 0)
    .rect(groove_d, groove_h)
    .extrude(length)
)

# Bottom grooves
bottom_groove1 = (
    cq.Workplane("XY")
    .center(-w / 2, -h / 2 + 1)
    .rect(slot_width, 2)
    .extrude(length)
)

bottom_groove2 = (
    cq.Workplane("XY")
    .center(w / 2, -h / 2 + 1)
    .rect(slot_width, 2)
    .extrude(length)
)

result = result.cut(bottom_groove1).cut(bottom_groove2)

# Chamfer edges slightly
result = (
    result
    .edges("|Z")
    .chamfer(0.5)
)