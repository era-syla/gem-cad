import cadquery as cq

# Parameters
L = 100   # overall length of base
W = 20    # width of base and vertical plate
T = 5     # thickness of plates
H = 40    # height of vertical plate
hole_dia = 6
margin = 25  # distance from each end to hole center

# Create base plate
base = cq.Workplane("XY").rect(L, W).extrude(T)

# Create vertical plate at one end of the base
vert = (
    cq.Workplane("YZ", origin=(-L/2, 0, T))
    .rect(W, H)
    .extrude(-T)
)

# Combine base and vertical plate into one solid
result = base.union(vert)

# Positions along X for the holes
x_positions = [-L/2 + margin, L/2 - margin]

# Drill holes through the base plate
for x in x_positions:
    result = (
        result
        .faces(">Z")
        .workplane()
        .pushPoints([(x, 0)])
        .hole(hole_dia, T + 1)
    )

# Drill holes through the vertical plate
for x in x_positions:
    cutter = (
        cq.Workplane("YZ", origin=(x, 0, T + H/2))
        .circle(hole_dia/2)
        .extrude(-(T + 1))
    )
    result = result.cut(cutter)