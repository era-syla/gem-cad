import cadquery as cq

# Parameters
L = 80      # length of top bar
W = 20      # width of top bar
T = 5       # thickness of top bar
H = 30      # height of side plates
ST = 5      # thickness of side plates
HR = 10     # radius of central arch
HD = 5      # diameter of top holes
SH = 5      # diameter of side-plate holes

# Create top bar
result = (
    cq.Workplane("XY")
    .box(L, W, T)
    .edges("|Z").fillet(2)
)

# Drill top holes
top_hole_positions = [(-25, 0), (-10, 0), (10, 0), (25, 0)]
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(top_hole_positions)
    .hole(HD)
)

# Cut central arch from bottom
result = (
    result
    .faces("<Z")
    .workplane()
    .center(0, 0)
    .circle(HR)
    .cutThruAll()
)

# Add side plates
for x_off in (-L/2 + ST/2, L/2 - ST/2):
    result = (
        result
        .faces("<Z")
        .workplane()
        .center(x_off, 0)
        .rect(ST, H)
        .extrude(H)
    )

# Drill holes through side plates
# Left plate
result = (
    result
    .faces("<X")
    .workplane()
    .pushPoints([(0, -H/2)])
    .hole(SH, ST*2)
)
# Right plate
result = (
    result
    .faces(">X")
    .workplane()
    .pushPoints([(0, -H/2)])
    .hole(SH, ST*2)
)