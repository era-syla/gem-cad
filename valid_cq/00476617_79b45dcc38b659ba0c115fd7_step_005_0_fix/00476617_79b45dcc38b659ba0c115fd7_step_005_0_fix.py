import cadquery as cq

T = 5       # plate thickness
H = 50      # plate height
Lx = 80     # length of X leg
Ly = 50     # length of Y leg
gus_w = 10  # gusset width along X
gus_off = 10 # gusset offset from ends along X
end_w = 5   # end flange width along Y
hole_d = 6  # hole diameter

# build the two main legs and the end flange
plate_x = cq.Workplane("XZ").rect(Lx, H).extrude(T)
plate_y = cq.Workplane("YZ").rect(Ly, H).extrude(-T)
plate_end = cq.Workplane("YZ", origin=(Lx, 0, 0)).rect(end_w, H).extrude(T)

result = plate_x.union(plate_y).union(plate_end)

# add two gussets (ribs) on the interior of the X leg
x1 = gus_off
x2 = Lx - gus_off - gus_w
gusset1 = cq.Workplane("XZ").transformed(offset=(x1, 0, 0)).rect(gus_w, H).extrude(-T)
gusset2 = cq.Workplane("XZ").transformed(offset=(x2, 0, 0)).rect(gus_w, H).extrude(-T)
result = result.union(gusset1).union(gusset2)

# drill two holes in the Y leg (left flange)
result = result.faces("<X").workplane().pushPoints([
    (0,  H/4),
    (0, -H/4),
]).hole(hole_d)

# drill two holes in the end flange (right flange)
result = result.faces(">X").workplane().pushPoints([
    (0,  H/4),
    (0, -H/4),
]).hole(hole_d)

# drill two holes in each gusset on the interior face of the X leg
pts = []
for x_c in (x1 + gus_w/2, x2 + gus_w/2):
    pts += [
        (x_c,  H/4),
        (x_c, 3*H/4),
    ]
result = result.faces("<Y").workplane().pushPoints(pts).hole(hole_d)