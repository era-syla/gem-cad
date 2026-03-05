import cadquery as cq

# Parameters
L = 80.0       # total length
W = 20.0       # width (depth of block)
H = 20.0       # height
jaw_len = L/2  # length of jaws / full-depth slot
gap_w = 10.0   # width of slot/groove
groove_depth = 2.0  # depth of the shallow groove on right half
hole_d = 5.0   # diameter of holes

# Build base block
result = cq.Workplane("XY").box(L, W, H)

# Full-depth slot on left half (creates two jaws)
result = (
    result
    .faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .transformed(offset=(-L/2 + jaw_len/2, 0, 0))
    .rect(jaw_len, gap_w)
    .cutThruAll()
)

# Shallow groove on right half
right_len = L - jaw_len
result = (
    result
    .faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .transformed(offset=(L/2 - right_len/2, 0, 0))
    .rect(right_len, gap_w)
    .cutBlind(-groove_depth)
)

# Holes on front face (left end)
z_off = H/4
result = (
    result
    .faces("<X")
    .workplane(centerOption="CenterOfMass")
    .pushPoints([( z_off, 0), (-z_off, 0)])
    .hole(hole_d)
)

# Hole on back face (right end)
result = (
    result
    .faces(">X")
    .workplane(centerOption="CenterOfMass")
    .pushPoints([(0, 0)])
    .hole(hole_d)
)