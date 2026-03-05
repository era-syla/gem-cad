import cadquery as cq

# Main body - elongated oval/stadium shape
length = 60
width = 20
height = 6
corner_r = 9

# Create main base body
base = (
    cq.Workplane("XY")
    .moveTo(-length/2 + corner_r, -width/2)
    .lineTo(length/2 - corner_r, -width/2)
    .threePointArc((length/2, 0), (length/2 - corner_r, width/2))
    .lineTo(-length/2 + corner_r, width/2)
    .threePointArc((-length/2, 0), (-length/2 + corner_r, -width/2))
    .close()
    .extrude(height)
)

# Add slight taper/raised platform on top
platform = (
    cq.Workplane("XY")
    .workplane(offset=height)
    .moveTo(-length/2 + corner_r + 2, -width/2 + 2)
    .lineTo(length/2 - corner_r - 2, -width/2 + 2)
    .threePointArc((length/2 - 2, 0), (length/2 - corner_r - 2, width/2 - 2))
    .lineTo(-length/2 + corner_r + 2, width/2 - 2)
    .threePointArc((-length/2 + 2, 0), (-length/2 + corner_r + 2, -width/2 + 2))
    .close()
    .extrude(1.5)
)

result = base.union(platform)

# Cut two rectangular slots (the characteristic openings)
slot_length = 18
slot_width = 8
slot_height = height + 2
slot_offset = 11

slot_left = (
    cq.Workplane("XY")
    .workplane(offset=-1)
    .center(-slot_offset, 0)
    .rect(slot_length, slot_width)
    .extrude(slot_height + 3)
)

slot_right = (
    cq.Workplane("XY")
    .workplane(offset=-1)
    .center(slot_offset, 0)
    .rect(slot_length, slot_width)
    .extrude(slot_height + 3)
)

result = result.cut(slot_left).cut(slot_right)

# Add center bridge/divider between slots (it's already there from the base)
# Add small connector tabs on the ends (left and right)
tab_length = 6
tab_width = 6
tab_height = 4

tab_left = (
    cq.Workplane("XY")
    .workplane(offset=height - tab_height)
    .center(-length/2 - tab_length/2 + 0.5, 0)
    .rect(tab_length, tab_width)
    .extrude(tab_height)
)

tab_right = (
    cq.Workplane("XY")
    .workplane(offset=height - tab_height)
    .center(length/2 + tab_length/2 - 0.5, 0)
    .rect(tab_length, tab_width)
    .extrude(tab_height)
)

result = result.union(tab_left).union(tab_right)

# Add small notch/hole in tabs
notch_size = 2.5

notch_left = (
    cq.Workplane("XY")
    .workplane(offset=height - tab_height - 1)
    .center(-length/2 - tab_length/2 + 0.5, 0)
    .rect(notch_size, notch_size)
    .extrude(tab_height + 2)
)

notch_right = (
    cq.Workplane("XY")
    .workplane(offset=height - tab_height - 1)
    .center(length/2 + tab_length/2 - 0.5, 0)
    .rect(notch_size, notch_size)
    .extrude(tab_height + 2)
)

result = result.cut(notch_left).cut(notch_right)

# Fillet the top edges of the main body
result = (
    result
    .edges("|Z")
    .fillet(1.0)
)