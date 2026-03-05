import cadquery as cq

# Parameters
L = 100    # total length
W = 20     # base width
H = 5      # base thickness
endL = 10  # length of end blocks
endEx = 4  # how much end blocks overhang in Y
pocketL = 40
pocketW = 12
pocketD = 3
tabRadius = 3
tabHole = 2
tabOffset = 25

# Base slab
result = cq.Workplane("XY").box(L, W, H)

# End blocks on both ends
endBlock = cq.Workplane("XY").box(endL, W + 2 * endEx, H)
result = result.union(endBlock.translate(( L/2 - endL/2, 0, 0)))
result = result.union(endBlock.translate((-L/2 + endL/2, 0, 0)))

# Central rectangular pocket from top
result = result.faces(">Z").workplane().rect(pocketL, pocketW).cutBlind(-pocketD)

# Circular hole through base (from top)
holeX = -L/4
result = result.faces(">Z").workplane().center(holeX, 0).hole(6)

# Tabs (half-cylinders) on top and their through-holes
for x in (tabOffset, -tabOffset):
    # full cylinder standing on the top face
    cyl = cq.Workplane("XY").workplane(offset=H).center(x, 0).circle(tabRadius).extrude(W)
    # cut away the bottom half of that cylinder to leave a half-cylinder
    cutBox = cq.Workplane("XY").box(2 * tabRadius, W + 2, H).translate((x, 0, H/2))
    cyl = cyl.cut(cutBox)
    result = result.union(cyl)
    # drill the hole through the half-cylinder, axis along Y
    holeCyl = (
        cq.Workplane("XY")
        .circle(tabHole / 2)
        .extrude(W + 2)
        .rotate((0, 0, 0), (1, 0, 0), -90)
        .translate((x, (W + 2) / 2, H + tabRadius))
    )
    result = result.cut(holeCyl)