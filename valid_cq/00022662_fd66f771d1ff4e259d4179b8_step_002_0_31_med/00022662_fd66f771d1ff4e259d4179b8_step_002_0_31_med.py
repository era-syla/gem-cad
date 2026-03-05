import cadquery as cq

# Parameters
R = 12.0
L = 48.0
D = 18.0
boss_h = 4.0
cyl_r = 8.5
cyl_l = 18.0
text_size = 10.0

# 1. Main body: box + left half-cylinder
# Create a composite sketch with a circle at the origin and a rectangle spanning to the right
s = cq.Sketch().rect(L, R*2).moved(cq.Location(cq.Vector(L/2, 0, 0)))
s = s.face(cq.Sketch().circle(R))

# Extrude the main body profile (goes in +Y direction by default for XZ workplane)
base = cq.Workplane("XZ").placeSketch(s).extrude(D)

# 2. Front cylindrical boss
# Centered at the origin, extending out the front face (-Y direction)
boss = (
    cq.Workplane("XZ", origin=(0, 0, 0))
    .workplane(offset=0.5)  # Start slightly inside to ensure a clean union
    .circle(R)
    .extrude(-boss_h - 0.5)
)

# 3. Right cylinder
# Attached to the right face, extending out to the right (+X direction)
right_cyl = (
    cq.Workplane("YZ", origin=(L - 0.5, D/2, 0))
    .circle(cyl_r)
    .extrude(cyl_l + 0.5)
)

# 4. Extruded Text "43D"
# Positioned on the flat section of the front face
text_geom = (
    cq.Workplane("XZ", origin=(30, 0, 0))
    .workplane(offset=0.5)
    .text("43D", fontsize=text_size, distance=-2.0)
)

# Combine all components into the final geometry
result = (
    base
    .union(boss.val())
    .union(right_cyl.val())
    .union(text_geom.val())
)

# Apply fillets to the leading edge of the front boss and the end edge of the right cylinder
result = result.edges("<Y").edges("%CIRCLE").fillet(1.0)
result = result.edges(">X").edges("%CIRCLE").fillet(1.0)
