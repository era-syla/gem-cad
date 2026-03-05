import cadquery as cq

# Parametric dimensions
thickness = 8.0
r_center = 18.0
r_ear = 10.0
l_ear = 28.0
r_hole_center = 11.0
r_hole_ear = 4.5
fillet_r = 6.0

# 1. Create the connecting rectangular body
rect_body = (
    cq.Workplane("XY")
    .rect(2 * l_ear, 2 * r_ear)
    .extrude(thickness)
)

# 2. Create the two ear cylinders
ears = (
    cq.Workplane("XY")
    .pushPoints([(-l_ear, 0), (l_ear, 0)])
    .circle(r_ear)
    .extrude(thickness)
)

# 3. Create the center cylinder
center = (
    cq.Workplane("XY")
    .circle(r_center)
    .extrude(thickness)
)

# 4. Combine shapes into a single solid body
body = rect_body.union(ears).union(center)

# 5. Fillet the 4 sharp concave vertical edges where the rectangle meets the center circle
# Calculate the exact X-coordinates of the intersections
x_int = (r_center**2 - r_ear**2)**0.5
z_mid = thickness / 2.0

# Define points near the 4 intersection edges to select them
pts = [
    (x_int, r_ear, z_mid),
    (x_int, -r_ear, z_mid),
    (-x_int, r_ear, z_mid),
    (-x_int, -r_ear, z_mid)
]

for p in pts:
    body = body.edges(cq.selectors.NearestToPointSelector(p)).fillet(fillet_r)

# 6. Cut the central and ear mounting holes
result = (
    body
    .faces(">Z").workplane()
    .circle(r_hole_center).cutThruAll()
    .faces(">Z").workplane()
    .pushPoints([(-l_ear, 0), (l_ear, 0)])
    .circle(r_hole_ear).cutThruAll()
)