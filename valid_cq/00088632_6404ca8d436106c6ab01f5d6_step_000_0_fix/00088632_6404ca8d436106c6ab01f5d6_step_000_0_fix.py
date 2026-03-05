import cadquery as cq

# Parameters
L = 120     # total length of the base block
W = 20      # width (Y direction)
H = 15      # height (Z direction)

leftLen = 35     # length of left solid block
pocketLen = 50   # length of recessed pocket in the center
rightLen = 35    # length of right solid block

pocketDepth = 8  # depth of the top pocket

plateTh = 2      # thickness of the side plates
rodDia = 4       # diameter of the rods
rodExt = 20      # extrusion length of the rods beyond the side plate

# Base block
result = cq.Workplane("XY").box(L, W, H)

# Cut the top pocket in the center
# The origin is at the center of the block, so the pocket center is at
# x = -L/2 + leftLen + pocketLen/2
pocketCenterX = -L/2 + leftLen + pocketLen/2
result = (
    result
    .faces(">Z")
    .workplane()
    .center(pocketCenterX, 0)
    .rect(pocketLen, W)
    .cutBlind(-pocketDepth)
)

# Compute the X position for the side plates (center of the right block)
plateCenterX = -L/2 + leftLen + pocketLen + rightLen/2

# Side plates (one on each side of the block)
plate1 = (
    cq.Workplane("XY")
    .box(rightLen, plateTh, H)
    .translate((plateCenterX,  W/2 + plateTh/2, H/2))
)
plate2 = (
    cq.Workplane("XY")
    .box(rightLen, plateTh, H)
    .translate((plateCenterX, -W/2 - plateTh/2, H/2))
)

result = result.union(plate1).union(plate2)

# Rods extruded from the outer face of the right block
# Outer face of right block is at x = -L/2 + leftLen + pocketLen + rightLen
rodStartX = -L/2 + leftLen + pocketLen + rightLen

# Two rods at different Z heights
z1 = H * 0.25
z2 = H * 0.75

rod1 = (
    cq.Workplane("YZ", origin=(rodStartX, 0, z1))
    .circle(rodDia/2)
    .extrude(rodExt)
)
rod2 = (
    cq.Workplane("YZ", origin=(rodStartX, 0, z2))
    .circle(rodDia/2)
    .extrude(rodExt)
)

result = result.union(rod1).union(rod2)