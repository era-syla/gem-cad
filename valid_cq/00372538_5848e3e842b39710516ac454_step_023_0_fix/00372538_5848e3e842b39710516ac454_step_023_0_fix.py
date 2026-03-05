import cadquery as cq

# Create main hollow cylinder
result = cq.Workplane("XY").circle(30).extrude(40)
result = result.faces("<Z").workplane().circle(26).cutBlind(40)

# Create top platform
result = result.faces(">Z").workplane().circle(28).extrude(8)

# Drill two small holes on platform
result = result.faces(">Z").workplane().pushPoints([(8.66, 5), (-8.66, 5)]).hole(4, 8)

# Create counterbore for large hole
result = result.faces(">Z").workplane().pushPoints([(17.32, -10)]).circle(7.5).cutBlind(-4)
# Drill the large through hole
result = result.faces(">Z").workplane().pushPoints([(17.32, -10)]).hole(10, 8)

# Add triangular wedge feature on top of platform
triangle = [(-5, 0), (5, 0), (0, 10)]
result = result.faces(">Z").workplane().polyline(triangle).close().extrude(8)

# Add cylindrical post on top
result = result.faces(">Z").workplane().circle(5).extrude(20)

# Cut out a radial notch in the side wall
cut = (
    cq.Workplane("XZ")
    .rect(10, 40)
    .extrude(40)
    .translate((15, 0, 20))
)
result = result.cut(cut)