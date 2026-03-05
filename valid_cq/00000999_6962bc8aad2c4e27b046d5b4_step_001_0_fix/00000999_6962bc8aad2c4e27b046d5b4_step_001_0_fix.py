import cadquery as cq

# Parameters
L = 240
W = 80
H = 25

slotW = 12
slotD = 15

ridgeW = 20
shoulderH = 12

recW = (W - ridgeW) / 2
recDepth = H - shoulderH

# Top hole pattern
N = 10
margin = 20
pitch = (L - 2 * margin) / (N - 1)
hd = 4

# End face holes
eh = 6
endHoleOffsetX = W / 2 - 10

# Build the base block
result = cq.Workplane("XY").box(L, W, H)

# Central slot
result = result.faces(">Z").workplane().rect(slotW, L).cutBlind(-slotD)

# Side recesses along top
for sign in (-1, 1):
    xOffset = sign * (ridgeW / 2 + recW / 2)
    result = result.faces(">Z").workplane().center(xOffset, 0).rect(recW, L).cutBlind(-recDepth)

# Top-line of holes through the ridge
top_hole_pts = [(0, -L/2 + margin + i * pitch) for i in range(N)]
result = result.faces(">Z").workplane().pushPoints(top_hole_pts).hole(hd, H + 1)

# Holes in the end faces
for face_sel in (">Y", "<Y"):
    pts = [(-endHoleOffsetX, 0), (endHoleOffsetX, 0)]
    result = result.faces(face_sel).workplane().pushPoints(pts).hole(eh, W + 1)

# Optional: fillet vertical edges for a smoother finish
result = result.edges("|Z").fillet(1)