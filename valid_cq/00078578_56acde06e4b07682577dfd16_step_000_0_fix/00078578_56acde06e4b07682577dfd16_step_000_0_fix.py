import cadquery as cq

# Parameters
main_dia = 20
main_len = 60
collar_dia = 24
collar_thickness = 4
rod_dia = 14
rod_len = 80
prong_th = 4
prong_h = 12
prong_len = 12
prong_gap = 6
hole_dia = 4
eye_dia = 10
eye_th = 4
eye_hole = 4

# Build main body
body = (
    cq.Workplane("XY")
    .circle(main_dia/2)
    .extrude(main_len)
    # front collar
    .faces("<Z")
    .workplane()
    .circle(collar_dia/2)
    .extrude(collar_thickness)
    # back collar
    .faces(">Z")
    .workplane()
    .circle(collar_dia/2)
    .extrude(collar_thickness)
    # back rod
    .faces(">Z")
    .workplane()
    .circle(rod_dia/2)
    .extrude(rod_len)
)

# Build front clevis prongs
y_off = (prong_gap + prong_th) / 2
prong1 = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .rect(prong_th, prong_h)
    .extrude(-prong_len)
    .translate((0, y_off, 0))
)
prong2 = prong1.translate((0, -2*y_off, 0))
clevis = prong1.union(prong2)

# Drill pin hole through prongs (hole axis = X)
clevis = (
    clevis
    .faces("<X")
    .workplane(centerOption="ProjectedOrigin")
    .workplane(offset=-prong_len/2)
    .circle(hole_dia/2)
    .cutThruAll()
)

# Build simple back eye (disc with hole)
eye = (
    cq.Workplane("XY")
    .workplane(offset=main_len + collar_thickness + rod_len)
    .circle(eye_dia/2)
    .extrude(eye_th)
    .faces(">Z")
    .workplane()
    .circle(eye_hole/2)
    .cutThruAll()
)

# Combine all
result = body.union(clevis).union(eye)