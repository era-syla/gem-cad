import cadquery as cq

# Parameters
L = 60     # total length of base
w = 20     # width of base
T = 10     # thickness of base
sw = 8     # slot width
R = 12     # cylinder radius
H = 30     # cylinder height
hr = 5     # hole radius in cylinder

# Build base capsule shape by union of rectangle and two semicircular ends
rect = cq.Workplane("XY").rect(L - w, w).extrude(T)
circ1 = cq.Workplane("XY").center(-(L - w)/2, 0).circle(w/2).extrude(T)
circ2 = cq.Workplane("XY").center((L - w)/2, 0).circle(w/2).extrude(T)
base = rect.union(circ1).union(circ2)

# Create slot shape (capsule) and cut it from the base
slot_len = L - w
slot_rect = base.faces(">Z").workplane().rect(slot_len, sw).extrude(-T)
slot_c1 = base.faces(">Z").workplane().center(-slot_len/2, 0).circle(sw/2).extrude(-T)
slot_c2 = base.faces(">Z").workplane().center( slot_len/2, 0).circle(sw/2).extrude(-T)
base = base.cut(slot_rect).cut(slot_c1).cut(slot_c2)

# Build cylinder with hole
cyl = cq.Workplane("XY").center((L - w)/2, 0).circle(R).extrude(H)
cyl = cyl.faces(">Z").workplane().hole(2*hr, H)

# Combine base and cylinder into final result
result = base.union(cyl)