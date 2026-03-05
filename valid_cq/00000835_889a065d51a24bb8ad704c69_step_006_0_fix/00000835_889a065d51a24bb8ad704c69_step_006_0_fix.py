import cadquery as cq

# Main plate dimensions
plate_length = 120
plate_width = 80
plate_thickness = 5

# Create the main plate
plate = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)

# Chamfer the bottom corners (all 4 corners of the plate)
plate = (
    plate
    .edges("|Z")
    .chamfer(5)
)

# Add mounting holes (4 corners)
hole_inset_x = 10
hole_inset_y = 10
hole_dia = 3.5

plate = (
    plate
    .faces(">Z")
    .workplane()
    .pushPoints([
        (plate_length/2 - hole_inset_x, plate_width/2 - hole_inset_y),
        (-plate_length/2 + hole_inset_x, plate_width/2 - hole_inset_y),
        (plate_length/2 - hole_inset_x, -plate_width/2 + hole_inset_y),
        (-plate_length/2 + hole_inset_x, -plate_width/2 + hole_inset_y),
    ])
    .circle(hole_dia / 2)
    .cutBlind(-plate_thickness)
)

# Add two raised blocks on the left side (top face)
block_width = 18
block_depth = 18
block_height = 15

# Block 1 - upper left
block1 = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(-plate_length/2 + 5, plate_width/2 - block_depth - 5, plate_thickness))
    .rect(block_width, block_depth, centered=False)
    .extrude(block_height)
)

# Block 2 - lower left (slightly lower position)
block2 = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(-plate_length/2 + 5, plate_width/2 - block_depth*2 - 12, plate_thickness))
    .rect(block_width, block_depth, centered=False)
    .extrude(block_height)
)

# Combine everything
result = plate.union(block1).union(block2)