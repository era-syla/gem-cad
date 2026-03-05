import cadquery as cq

# Parameters
L = 80          # total length in X
R_end = 10      # radius of end semicircles
W = 20          # width in Y
H = 15          # height in Z
R_inner = 8     # radius of inner groove
D_hole = 5      # diameter of holes

# Build the main body: center block + two end semicylinders
mid_length = L - 2 * R_end
mid = cq.Workplane("XY").rect(mid_length, W).extrude(H)
c1 = cq.Workplane("XY").circle(R_end).extrude(H).translate((-L/2, 0, 0))
c2 = cq.Workplane("XY").circle(R_end).extrude(H).translate(( L/2, 0, 0))
result = mid.union(c1).union(c2)

# Cut the inner semicylindrical groove
groove = (
    cq.Workplane("ZX")
    .center(0, H)
    .circle(R_inner)
    .extrude(W * 2)
    .translate((0, -W, 0))
)
result = result.cut(groove)

# Drill through holes at the centers of the end semicircles
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(-L/2, 0), (L/2, 0)])
    .hole(H + 1, D_hole)
)