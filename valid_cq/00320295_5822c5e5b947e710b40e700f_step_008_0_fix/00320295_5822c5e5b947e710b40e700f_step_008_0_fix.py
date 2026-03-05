import cadquery as cq

# Parameters
bw = 20    # block width (X)
bh = 60    # block height (Z)
bd = 10    # block depth (Y)
pw = 8     # pocket width
ph = 40    # pocket height
pd = 5     # pocket depth
prongD = 8 # prong extrusion depth (along Y)
prongW = 4 # prong width (X)
prongH = 10# prong height (Z)
# Z positions for top and bottom prongs
tpoz = bh/2 - prongH/2
bpoz = -tpoz

# Build main block
result = cq.Workplane("XZ").rect(bw, bh).extrude(bd)

# Cut rectangular pocket on back face (Y<0 side)
result = result.faces("<Y").workplane().rect(pw, ph).cutBlind(pd)

# Add prongs (two top, three bottom) on front face (Y>0 side)
prong_positions = [(-bw/4, tpoz), ( bw/4, tpoz),
                   (-bw/4, bpoz), (    0, bpoz), ( bw/4, bpoz)]
result = result.faces(">Y").workplane().pushPoints(prong_positions).rect(prongW, prongH).extrude(prongD)

# Drill holes through the two top prongs (axis along X)
hole_r = 2
# position in Y where prongs are centered
y_c = bd + prongD/2
# length to extrude cylinder so it clears the block
hole_len = bw + 4
for x_c, z_c in [(-bw/4, tpoz), (bw/4, tpoz)]:
    cutter = cq.Workplane("YZ", origin=(-bw/2 - 2, y_c, z_c)).circle(hole_r).extrude(hole_len)
    result = result.cut(cutter)