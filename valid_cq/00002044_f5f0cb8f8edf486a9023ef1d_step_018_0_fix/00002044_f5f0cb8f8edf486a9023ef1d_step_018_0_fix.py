import cadquery as cq

# Parameters
L, W, H = 60, 30, 20
wall = 2
pin_r = 0.5
pin_len = 5
cols, rows = 8, 4
pin_spacing = 3
radii = [10, 15, 20, 25]
rib_thickness = wall
rib_height = 8

# Outer box
outer = cq.Workplane("XY").box(L, W, H)

# Hollow out sides and bottom, leave open top
inner = cq.Workplane("XY").box(L - 2*wall, W - 2*wall, H - wall).translate((
    0,
    0,
    H/2 - (H - wall)/2,
))
box = outer.cut(inner)

# Front rectangular opening for pins
rec_w = (cols - 1)*pin_spacing + 2*pin_spacing
rec_h = (rows - 1)*pin_spacing + 2*pin_spacing
box = box.faces("<X").workplane().center(wall, 0).rect(rec_w, rec_h).cutThruAll()

# Pins
pts = []
for i in range(cols):
    for j in range(rows):
        y = (i - (cols - 1)/2)*pin_spacing
        z = (j - (rows - 1)/2)*pin_spacing
        pts.append((y, z))
box = box.faces("<X").workplane().center(wall, 0).pushPoints(pts).circle(pin_r).extrude(-pin_len)

# Ribs inside the open top
cx = -L/2 + wall
cy = -W/2 + wall
ribs = None
for r_out in radii:
    r_in = r_out - rib_thickness
    rib = (
        cq.Workplane("XY", origin=(cx, cy, -H/2 + wall))
        .moveTo(r_out, 0)
        .threePointArc((0, r_out), (r_out, r_out))
        .lineTo(0, r_in)
        .threePointArc((r_in, 0), (r_in, r_in))
        .close()
        .extrude(rib_height)
    )
    if ribs is None:
        ribs = rib
    else:
        ribs = ribs.union(rib)

result = box.union(ribs)