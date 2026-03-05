import cadquery as cq

length = 60
foot = 10
height = 30
width = 12
fillet_r = 2
hex_dia = 8

# 2D side profile in X-Z plane
profile = [
    (0, 0),
    (foot, 0),
    (length/2, height),
    (length-foot, 0),
    (length, 0),
]

# Build bracket by extruding profile in Y direction
result = (
    cq.Workplane("XZ")
    .polyline(profile)
    .close()
    .extrude(width)
    .edges()
    .fillet(fillet_r)
)

# Cut hex hole through thickness at the apex region
result = (
    result
    .faces(">Y")
    .workplane()
    .pushPoints([(length/2, height * 0.5)])
    .polygon(6, hex_dia)
    .cutThruAll()
)

# Add internal triangular pocket from the back face
pocket = [
    (foot, 0),
    (length/2, height * 0.6),
    (length - foot, 0),
]
result = (
    result
    .faces("<Y")
    .workplane()
    .polyline(pocket)
    .close()
    .cutBlind(width / 2)
)