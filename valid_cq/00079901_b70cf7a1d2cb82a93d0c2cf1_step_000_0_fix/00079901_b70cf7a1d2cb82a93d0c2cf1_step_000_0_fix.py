import cadquery as cq

flat2flat = 20
Lr = 30
W = flat2flat
H = 10
R = H
hex_cx = -flat2flat/2

rect = cq.Workplane("XY").rect(Lr, W).extrude(H).translate((Lr/2, 0, 0))
hexp = cq.Workplane("XY").center(hex_cx, 0).polygon(6, flat2flat).extrude(H)
result = rect.union(hexp)

cut_cyl = cq.Workplane("XZ").workplane(offset=-W/2).circle(R).extrude(W)
result = result.cut(cut_cyl)

result = result.faces(">Z and <X").workplane().hole(10)