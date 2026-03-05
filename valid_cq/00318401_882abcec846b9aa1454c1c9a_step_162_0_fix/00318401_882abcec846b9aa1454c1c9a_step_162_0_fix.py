import cadquery as cq

# Parameters
L = 200     # Plate length
W = 80      # Plate width
H = 10      # Plate thickness
tab_l = 15  # Tab length (along X)
tab_w = 10  # Tab width (along Y)
tab_h = 8   # Tab height (along Z)
hole_central_d = 6
hole_side_d = 4
hole_tab_d = 5

# Base plate
base = cq.Workplane("XY").rect(L, W).extrude(H)

# Tabs
tab1 = (
    cq.Workplane("XY")
    .transformed(offset=(L/2 - tab_l/2,  W/2 - tab_w/2, H))
    .rect(tab_l, tab_w)
    .extrude(tab_h)
)
tab2 = (
    cq.Workplane("XY")
    .transformed(offset=(L/2 - tab_l/2, -W/2 + tab_w/2, H))
    .rect(tab_l, tab_w)
    .extrude(tab_h)
)

# Combine base and tabs
result = base.union(tab1).union(tab2)

# Central top hole
result = result.faces(">Z").workplane().hole(hole_central_d, depth=H + tab_h)

# Side holes in the main plate on the positive Y face
mid_pts = [(-50, H/2), (50, H/2)]
result = result.faces(">Y").workplane().pushPoints(mid_pts).hole(hole_side_d, depth=W + 20)

# Tab holes on the positive Y face
tab_hole_pos = (L/2 - tab_l/2, H + tab_h/2)
result = result.faces(">Y").workplane().pushPoints([tab_hole_pos]).hole(hole_tab_d, depth=W + 20)

# Tab holes on the negative Y face
result = result.faces("<Y").workplane().pushPoints([tab_hole_pos]).hole(hole_tab_d, depth=W + 20)