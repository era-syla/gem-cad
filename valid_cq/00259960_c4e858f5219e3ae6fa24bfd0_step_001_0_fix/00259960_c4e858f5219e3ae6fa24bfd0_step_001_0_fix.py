import cadquery as cq

result = cq.Workplane("XZ").polyline([
    (0, 0),
    (120, 0),
    (155, 20),
    (160, 20),
    (0, 20)
]).close().extrude(10)

# Fillet the long edges (handle rounding)
result = result.edges("|Z").fillet(3)

# Drill the handle hole at the narrow end
result = result.faces("<X").workplane().hole(6)

# Cut fixed jaw slot on the front face
result = result.faces(">Y").workplane().center(142, 12).rect(30, 6).cutThruAll()

# Cut movable jaw slot on the front face
result = result.faces(">Y").workplane().center(150, 7).rect(12, 4).cutThruAll()

# Add a simple adjustment screw shape (cylinder) in the movable jaw
result = result.faces(">Y").workplane().center(150, 7).circle(2).extrude(-10)