import cadquery as cq

W = 20.0
H = 20.0
wall = 1.5
slot_w = 6.0
slot_depth = 6.0
L = 200.0

result = cq.Workplane("XY").rect(W, H).extrude(L)
result = result.faces(">Z").workplane().rect(W-2*wall, H-2*wall).cutBlind(-L)

result = result.faces(">X").workplane(centerOption="CenterOfMass").rect(slot_w, H-2*wall).cutBlind(-slot_depth)
result = result.faces("<X").workplane(centerOption="CenterOfMass").rect(slot_w, H-2*wall).cutBlind(-slot_depth)
result = result.faces(">Y").workplane(centerOption="CenterOfMass").rect(W-2*wall, slot_w).cutBlind(-slot_depth)
result = result.faces("<Y").workplane(centerOption="CenterOfMass").rect(W-2*wall, slot_w).cutBlind(-slot_depth)