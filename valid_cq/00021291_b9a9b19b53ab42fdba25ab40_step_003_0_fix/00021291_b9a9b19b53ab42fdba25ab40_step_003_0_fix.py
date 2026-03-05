import cadquery as cq

# Parameters
L = 80         # total width in X
T = 10         # thickness in Y
base = 5       # base height in Z
height = 55    # total height in Z
top_w = 20     # top flange width in X
pocket_w = 10  # pocket width in X
pocket_d = 2   # pocket depth in Y
hole_d = 5     # hole diameter
hole_count = 6
margin = 10    # margin from top/bottom for holes

# Compute hole positions
z_start = base + margin
spacing = (height - base - 2*margin) / (hole_count - 1)
z_positions = [z_start + i*spacing for i in range(hole_count)]

# 2D profile in the X-Z plane
profile = [
    (0, 0),
    (L, 0),
    (L, base),
    (L - (L - top_w) / 2, height),
    ((L - top_w) / 2, height),
    (0, base),
]

# Build the extruded shape
result = cq.Workplane("XZ") \
    .polyline(profile).close() \
    .extrude(T)

# Cut the central pocket on the front face
result = result.faces(">Y") \
    .workplane(origin=(0, 0, base)) \
    .rect(pocket_w, height - base) \
    .cutBlind(-pocket_d)

# Drill the holes through the thickness
points = [(0, z) for z in z_positions]
result = result.faces(">Y") \
    .workplane(origin=(0, 0, base)) \
    .pushPoints(points) \
    .hole(hole_d)

# 'result' now holds the final solid geometry