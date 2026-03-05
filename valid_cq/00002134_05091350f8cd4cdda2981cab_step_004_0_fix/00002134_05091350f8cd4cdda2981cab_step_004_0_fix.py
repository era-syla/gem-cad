import cadquery as cq

# Parameters
cube_size = 40
pocket_width = 32
pocket_height = 8
pocket_depth = 6
corner_hole_d = 3
corner_offset = 15
plate_diameter = 30
plate_thickness = 4
shaft_diameter = 6
shaft_length = 20

# Build base cube
result = (
    cq.Workplane("XY")
    .box(cube_size, cube_size, cube_size)
    # Side pockets on ±X and ±Y faces
    .faces(">X").workplane().rect(pocket_width, pocket_height).cutBlind(-pocket_depth)
    .faces("<X").workplane().rect(pocket_width, pocket_height).cutBlind(-pocket_depth)
    .faces(">Y").workplane().rect(pocket_width, pocket_height).cutBlind(-pocket_depth)
    .faces("<Y").workplane().rect(pocket_width, pocket_height).cutBlind(-pocket_depth)
    # Corner holes on top face
    .faces(">Z").workplane()
    .pushPoints([
        (-corner_offset, -corner_offset),
        ( corner_offset, -corner_offset),
        ( corner_offset,  corner_offset),
        (-corner_offset,  corner_offset),
    ])
    .hole(corner_hole_d)
    # Top circular plate
    .faces(">Z").workplane()
    .circle(plate_diameter/2).extrude(plate_thickness)
    # Shaft on top of plate
    .faces(">Z").workplane()
    .circle(shaft_diameter/2).extrude(shaft_length)
)

# At this point, 'result' holds the final solid geometry.