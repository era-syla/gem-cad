import cadquery as cq

# Parameters
L = 120    # total length
W = 40     # total width
T = 5      # base thickness
Lf = 20    # flange length each end
R = 20     # cradle radius
centralLen = L - 2 * Lf
blockLen = 10
blockH = 10
slotLen = 20
slotW = 4
slotDepth = blockH / 2
holeD = 5

# Build base and central support
result = cq.Workplane("XY").box(L, W, T)
result = result.faces(">Z").workplane().rect(centralLen, W).extrude(R)

# Subtract half‐cylinder channel
cyl_cut = cq.Workplane("YZ", origin=(0, 0, T)).circle(R).extrude(centralLen)
result = result.cut(cyl_cut)

# Add raised blocks at ends of the support
for x in (-centralLen / 2, centralLen / 2):
    result = result.faces(">Z").workplane().center(x, 0).rect(blockLen, W).extrude(blockH)

# Cut rectangular slots in the raised blocks
ySlot = (W - slotW) / 2
for y in (ySlot, -ySlot):
    result = result.faces(">Z").workplane().center(0, y).rect(slotLen, slotW).cutBlind(slotDepth)

# Add mounting holes through the flanges on both ends
for faceSel in ("<X", ">X"):
    result = result.faces(faceSel).workplane().pushPoints([(0, W/4), (0, -W/4)]).hole(holeD)