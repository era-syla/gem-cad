import cadquery as cq

# Parameters
L1, L2, h, t, W = 150, 60, 50, 5, 40

# Cross‐section outline in the YZ plane
pts = [
    (-L1,    0),
    (-L1,   -t),
    (   0,   -t),
    (   0, -(h + t)),
    (  L2, -(h + t)),
    (  L2,   -h),
    (   0,   -h),
    (   0,     0),
]

# Create the bent bracket by extruding the profile in X
result = cq.Workplane("YZ").polyline(pts).close().extrude(W)

# Hole pattern on the top flange
cols = 3
rows = 5
mx = 8
my = 20
sx = (W - 2*mx) / (cols - 1)
sy = (L1 - 2*my) / (rows - 1)
xpos = [mx + i*sx for i in range(cols)]
ypos = [-L1 + my + j*sy for j in range(rows)]
top_hole_pts = [(x, y) for y in ypos for x in xpos]

# Drill through-thickness holes on top flange
result = result.faces(">Z").workplane().pushPoints(top_hole_pts).hole(W + 1)

# Hole pattern on the foot flange
myf = 12
ypos_f = [myf, L2 - myf]
foot_hole_pts = [(x, y) for y in ypos_f for x in xpos]

# Drill through-thickness holes on foot flange
result = result.faces("<Z").workplane().pushPoints(foot_hole_pts).hole(W + 1)