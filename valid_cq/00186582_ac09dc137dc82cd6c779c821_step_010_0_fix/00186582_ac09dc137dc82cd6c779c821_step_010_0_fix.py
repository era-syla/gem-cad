import cadquery as cq

# Parameters
thk = 4
outerW1 = 80
outerH1 = 50
outerW2 = 50
outerH2 = 60
frameT = 5
gap = 20
strutW = 10
holeD = 4
channelH = 10
channelW = outerW1 - 2*frameT - 10

# Derived
innerW1 = outerW1 - 2*frameT
innerH1 = outerH1 - 2*frameT
innerW2 = outerW2 - 2*frameT
innerH2 = outerH2 - 2*frameT
topY = outerH1/2 + gap + outerH2/2
strutY = outerH1/2 + gap/2
strutXpos = outerW2/2 - strutW/2
chanY = -outerH1/2 + frameT + channelH/2

# Bottom frame
bottom = cq.Workplane("XY").rect(outerW1, outerH1).extrude(thk)

# Top frame
top = cq.Workplane("XY").center(0, topY).rect(outerW2, outerH2).extrude(thk)

# Struts
strut1 = cq.Workplane("XY").box(strutW, gap, thk, centered=(True, True, False)).translate((strutXpos, strutY, 0))
strut2 = strut1.mirror("YZ")

# Combine solids
result = bottom.union(top).union(strut1).union(strut2)

# Inner cutouts
cut1 = cq.Workplane("XY").rect(innerW1, innerH1).extrude(thk+1)
cut2 = cq.Workplane("XY").center(0, topY).rect(innerW2, innerH2).extrude(thk+1)
result = result.cut(cut1).cut(cut2)

# Channel cut in bottom frame
chan = cq.Workplane("XY").center(0, chanY).rect(channelW, channelH).extrude(thk+1)
result = result.cut(chan)

# Holes: bottom corners
hc = frameT/2
pts = [
    ( outerW1/2 - hc,  outerH1/2 - hc),
    (-outerW1/2 + hc,  outerH1/2 - hc),
    ( outerW1/2 - hc, -outerH1/2 + hc),
    (-outerW1/2 + hc, -outerH1/2 + hc),
]
# Holes: top ears (only two)
pts += [
    ( outerW2/2 - hc, topY + outerH2/2 - hc),
    (-outerW2/2 + hc, topY + outerH2/2 - hc),
]
# Holes: strut midpoints
pts += [
    ( strutXpos, strutY),
    (-strutXpos, strutY),
]

# Create holes through thickness
result = result.faces(">Z").workplane().pushPoints(pts).circle(holeD/2).cutThruAll()

# Final result
result