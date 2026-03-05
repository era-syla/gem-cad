import cadquery as cq

# Parameters
plate_len = 80
plate_wid = 50
plate_thk = 4

tab_ext = 5
tab_len = 20

pocket_w = 15
pocket_dy = 6
pocket_depth = 2

hole_d = 10

# Base plate
result = cq.Workplane("XY").box(plate_len, plate_wid, plate_thk)

# Back long-edge central tab
result = result.union(
    cq.Workplane("XY")
      .box(tab_len, tab_ext, plate_thk)
      .translate((0, plate_wid/2 + tab_ext/2, 0))
)

# Left short-edge central tab
result = result.union(
    cq.Workplane("XY")
      .box(tab_ext, tab_len, plate_thk)
      .translate((-plate_len/2 - tab_ext/2, 0, 0))
)

# Right short-edge central tab
result = result.union(
    cq.Workplane("XY")
      .box(tab_ext, tab_len, plate_thk)
      .translate((plate_len/2 + tab_ext/2, 0, 0))
)

# Rectangular pockets on front edge
result = result.faces(">Z").workplane().pushPoints([
    (-plate_len/4, -plate_wid/2 + pocket_dy/2),
    ( plate_len/4, -plate_wid/2 + pocket_dy/2)
]).rect(pocket_w, pocket_dy).cutBlind(-pocket_depth)

# Circular through holes
result = result.faces(">Z").workplane().pushPoints([
    (-plate_len/4, 0),
    ( plate_len/4, 0)
]).hole(hole_d)