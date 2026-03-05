import cadquery as cq

# Parameters
plate_length = 100.0
plate_height = 20.0
plate_thickness = 3.0
radius = plate_height / 2.0
straight_length = plate_length - 2 * radius

block_width = 20.0
block_height = 8.0
block_depth = 10.0

# Base plate: a straight rectangle plus two semicircular ends, extruded in Y
plate = (
    cq.Workplane("XZ")
    .center(0, 0)
    .rect(straight_length, plate_height)
    .extrude(plate_thickness)
    .union(
        cq.Workplane("XZ")
        .center(straight_length / 2.0, 0)
        .circle(radius)
        .extrude(plate_thickness)
    )
    .union(
        cq.Workplane("XZ")
        .center(-straight_length / 2.0, 0)
        .circle(radius)
        .extrude(plate_thickness)
    )
)

# Add the rectangular block on the front face, flush to top edge
plate = plate.union(
    plate.faces(">Y")
    .workplane()
    .center(0, (plate_height - block_height) / 2.0)
    .rect(block_width, block_height)
    .extrude(block_depth)
)

result = plate