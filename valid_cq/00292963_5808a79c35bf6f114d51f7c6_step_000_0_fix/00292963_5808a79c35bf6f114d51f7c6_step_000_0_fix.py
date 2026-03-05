import cadquery as cq

plate_thickness = 4
plate_width = 64
plate_height = 42
side_thickness = 4
side_depth = 20
hole_radius = 10
ellipse_rx = 20
ellipse_ry = 8

# front plate
plate = cq.Workplane("XY").rect(plate_width, plate_height).extrude(plate_thickness)

# central elliptical cutout
plate = plate.faces(">Z").workplane().ellipse(ellipse_rx, ellipse_ry).cutThruAll()

# side supports
left = (
    cq.Workplane("XY")
    .transformed(offset=(-plate_width/2 + side_thickness/2, 0, plate_thickness/2), rotate=(0, 90, 0))
    .rect(side_depth, plate_height)
    .extrude(side_thickness)
)
right = (
    cq.Workplane("XY")
    .transformed(offset=(plate_width/2 - side_thickness/2, 0, plate_thickness/2), rotate=(0, 90, 0))
    .rect(side_depth, plate_height)
    .extrude(side_thickness)
)

result = plate.union(left).union(right)

# circular holes in side supports
result = (
    result
    .faces("<Y")
    .workplane()
    .pushPoints([(-plate_width/2 + side_thickness, 0), (plate_width/2 - side_thickness, 0)])
    .circle(hole_radius)
    .cutThruAll()
)

# keyhole-style mounting holes on front plate (simple round)
slot_positions = [
    (-plate_width/2 + 8, -plate_height/2 + 8),
    ( plate_width/2 - 8, -plate_height/2 + 8),
]
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(slot_positions)
    .circle(3)
    .cutBlind(-plate_thickness)
)

# cut text "CLEK" into front face
result = (
    result
    .faces(">Z")
    .workplane()
    .transformed(offset=(0, -plate_height/2 + 10, 0))
    .text("CLEK", 6, 1, cut=True)
)