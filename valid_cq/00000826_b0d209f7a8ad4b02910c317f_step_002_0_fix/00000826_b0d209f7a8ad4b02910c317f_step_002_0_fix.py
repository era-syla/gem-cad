import cadquery as cq

# Main body dimensions
body_w = 40
body_d = 38
body_h = 14

# Create the main rectangular body with rounded corners
main_body = (
    cq.Workplane("XY")
    .rect(body_w, body_d)
    .extrude(body_h)
)

# Round the top edges and vertical edges
main_body = (
    main_body
    .edges("|Z")
    .fillet(4)
    .edges(">Z")
    .fillet(2)
)

# Add the oval/pill-shaped tab on the left side
tab_w = 10
tab_d = 18
tab_h = body_h

tab = (
    cq.Workplane("XY")
    .center(-body_w/2 - tab_w/2 + 2, 0)
    .rect(tab_w, tab_d)
    .extrude(tab_h)
)

tab = (
    tab
    .edges("|Z")
    .fillet(4.5)
    .edges(">Z")
    .fillet(1.5)
)

# Union the tab with the main body
combined = main_body.union(tab)

# Create the large rectangular pocket on top
pocket_w = 28
pocket_d = 26
pocket_depth = 8

combined = (
    combined
    .faces(">Z")
    .workplane()
    .center(2, 0)
    .rect(pocket_w, pocket_d)
    .cutBlind(-pocket_depth)
)

# Create the central divider/rib inside the pocket
rib_w = 6
rib_d = 26
rib_h = pocket_depth - 3

combined = (
    combined
    .faces(">Z[-2]")
    .workplane()
    .center(2, 0)
    .rect(rib_w, rib_d)
    .extrude(rib_h)
)

# Cut the oval hole in the left tab
tab_hole_w = 5
tab_hole_d = 12
tab_hole_depth = body_h - 3

combined = (
    combined
    .faces(">Z")
    .workplane()
    .center(-body_w/2 - tab_w/2 + 2, 0)
    .rect(tab_hole_w, tab_hole_d)
    .cutBlind(-tab_hole_depth)
)

# Round the hole edges
combined = (
    combined
    .faces("<Z[-2]")
    .edges()
    .fillet(2)
)

result = combined