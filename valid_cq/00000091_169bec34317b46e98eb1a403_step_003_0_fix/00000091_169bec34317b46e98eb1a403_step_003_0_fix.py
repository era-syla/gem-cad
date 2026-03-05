import cadquery as cq

# Main body dimensions
length = 60
width = 30
height = 20
radius = width / 2  # 15

# Create the main stadium-shaped body (rounded rectangle / discorectangle)
main_body = (
    cq.Workplane("XY")
    .moveTo(-length/2 + radius, 0)
    .lineTo(length/2 - radius, 0)
    .threePointArc((length/2, radius), (length/2 - radius, width/2))
    .lineTo(-length/2 + radius, width/2)
    .threePointArc((-length/2, radius), (-length/2 + radius, 0))
    .close()
    .extrude(height)
)

# Create stadium shape profile using a cleaner approach
def make_stadium(l, w, h):
    r = w / 2
    result = (
        cq.Workplane("XY")
        .center(0, w/2)
        .workplane()
    )
    # Use slot/pill shape
    body = (
        cq.Workplane("XY")
        .rect(l - w, w)
        .extrude(h)
    )
    cyl1 = cq.Workplane("XY").center((l - w)/2, 0).circle(w/2).extrude(h)
    cyl2 = cq.Workplane("XY").center(-(l - w)/2, 0).circle(w/2).extrude(h)
    return body.union(cyl1).union(cyl2)

main_body = make_stadium(length, width, height)

# Create the top lid - stadium shape, slightly larger, thinner
lid_thickness = 3
lid_overhang = 1

lid_body = make_stadium(length + lid_overhang*2, width + lid_overhang*2, lid_thickness)
lid = lid_body.translate((0, 0, height))

# The lid top surface - half rounded (semicircle on one end, flat on other)
# Create a lid that is flat on left side and rounded on right
lid_length = length + lid_overhang * 2
lid_width = width + lid_overhang * 2
lid_r = lid_width / 2

# Build custom lid shape: flat on left, semicircle on right
lid_custom = (
    cq.Workplane("XY")
    .moveTo(-lid_length/2, -lid_r)
    .lineTo(lid_length/2 - lid_r, -lid_r)
    .threePointArc((lid_length/2, 0), (lid_length/2 - lid_r, lid_r))
    .lineTo(-lid_length/2, lid_r)
    .close()
    .extrude(lid_thickness)
    .translate((0, 0, height))
)

# Small cylinder/tab on the left side of lid
tab_r = 5
tab_h = height
tab = (
    cq.Workplane("XY")
    .center(-length/2 - lid_overhang - tab_r + 2, 0)
    .circle(tab_r)
    .extrude(tab_h)
)

# Groove on the right side of the main body
groove_w = 15
groove_h = 3
groove_d = 2

groove = (
    cq.Workplane("XY")
    .center(length/2 - 5, 0)
    .workplane(offset=height - groove_h - 2)
    .rect(groove_d, groove_w)
    .extrude(groove_h)
)

# Horizontal slot on right face
slot = (
    cq.Workplane("YZ")
    .center(0, height/2)
    .workplane()
    .center(length/2, height/2)
)

slot_cut = (
    cq.Workplane("XZ")
    .center(0, height - 5)
    .rect(groove_w, groove_h / 2)
    .extrude(groove_d)
    .translate((length/2 - groove_d, 0, 0))
)

# Assemble
result = (
    main_body
    .union(lid_custom)
    .union(tab)
    .cut(slot_cut)
)

# Add a horizontal slot cut on the right side
slot_cut2 = (
    cq.Workplane("YZ")
    .center(0, height - 4)
    .rect(groove_w, 2)
    .extrude(3)
    .translate((length/2 - 3, 0, 0))
)

result = result.cut(slot_cut2)