import cadquery as cq

# parameters
base_size = 100
base_thickness = 3
top_size = 80
top_thickness = 4
hole_diameter = 5
hole_offset = 10
square_cut_size = 10
square_cut_offset = 20
tab_width = 20
tab_extension = 6
slot_width = 4
slot_height = 2

# base plate
base = cq.Workplane("XY").box(base_size, base_size, base_thickness)

# top plate
top = cq.Workplane("XY") \
    .transformed(offset=(0, 0, base_thickness)) \
    .box(top_size, top_size, top_thickness)

# tabs on left and right
tabs = None
for sign in (-1, 1):
    tab = cq.Workplane("XY") \
        .transformed(offset=(sign*(top_size/2 + tab_extension/2), 0, base_thickness + top_thickness/2)) \
        .box(tab_extension, tab_width, top_thickness)
    tabs = tab if tabs is None else tabs.union(tab)

# assemble base, top, and tabs
model = base.union(top).union(tabs)

# four round holes through top plate and base
d = top_size/2 - hole_offset
hole_points = [(-d, -d), (-d, d), (d, -d), (d, d)]
model = model.faces(">Z").workplane().pushPoints(hole_points).hole(hole_diameter)

# two square cutouts through top plate
square_points = [(-square_cut_offset, 0), (square_cut_offset, 0)]
model = model.faces(">Z").workplane() \
    .pushPoints(square_points) \
    .rect(square_cut_size, square_cut_size) \
    .cutBlind(-top_thickness)

# slots through the tabs
for sign in (-1, 1):
    slot = cq.Workplane("XY") \
        .box(tab_extension+2, slot_width, top_thickness) \
        .translate((sign*(top_size/2 + tab_extension/2), 0, base_thickness + top_thickness/2))
    model = model.cut(slot)

result = model