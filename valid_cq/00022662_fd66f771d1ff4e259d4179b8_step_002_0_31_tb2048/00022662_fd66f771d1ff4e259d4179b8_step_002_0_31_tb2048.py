import cadquery as cq

# Dimensions
height = 20.0
width = 30.0
depth = 15.0
boss_radius = height / 2.0
boss_extrude = 2.0
cyl_radius = 7.5
cyl_length = 15.0

# 1. Create the main body (profile in XZ plane, extruded along -Y)
base = (
    cq.Workplane("XZ")
    .moveTo(0, height/2)
    .lineTo(width, height/2)
    .lineTo(width, -height/2)
    .lineTo(0, -height/2)
    .threePointArc((-boss_radius, 0), (0, height/2))
    .close()
    .extrude(-depth)
)

# 2. Add the circular boss on the front face (Y=0)
boss = cq.Workplane("XZ").circle(boss_radius).extrude(boss_extrude)
body = base.union(boss)

# 3. Fillet the front edge of the boss
body = body.faces(">Y").edges().fillet(1.0)

# 4. Add the right cylinder protruding from X=30
right_cyl = (
    cq.Workplane("YZ")
    .workplane(offset=width)
    .center(-depth/2, 0)
    .circle(cyl_radius)
    .extrude(cyl_length)
)
body = body.union(right_cyl)

# 5. Fillet the outer edge of the right cylinder
body = body.faces(">X").edges().fillet(1.0)

# 6. Add the embossed text "43D" on the front face
text_shape = (
    cq.Workplane("XZ")
    .center(16.5, 0)
    .text("43D", fontsize=7.5, distance=1.0, halign="center", valign="center")
)

# Final model
result = body.union(text_shape)