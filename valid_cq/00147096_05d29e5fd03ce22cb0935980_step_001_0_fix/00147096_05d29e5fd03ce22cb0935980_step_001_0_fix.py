import cadquery as cq

# Parameters for frame
L = 120
W = 80
h = 4
t = 3
Rc = 20

# Build the rectangular loop frame
frame_outer = cq.Workplane("XY").box(L, W, h, centered=(True, True, False))
frame = frame_outer.edges("|Z").fillet(Rc)
inner_cut = cq.Workplane("XY").box(L - 2 * t, W - 2 * t, h + 2, centered=(True, True, False)).translate((0, 0, -1))
frame = frame.cut(inner_cut)

# Parameters for trough
Lt = L - 40
Wt = 20
roof_thickness = 4
wall_thickness = 3
wall_height = 15

# Build the trough roof
roof = cq.Workplane("XY").workplane(offset=h).rect(Lt, Wt).extrude(roof_thickness)

# Build the side walls of the trough
y_off = Wt / 2 - wall_thickness / 2
pts = [(0, y_off), (0, -y_off)]
walls = roof.faces("<Z").workplane().pushPoints(pts).rect(Lt, wall_thickness).extrude(-wall_height)

trough = roof.union(walls)

result = frame.union(trough)