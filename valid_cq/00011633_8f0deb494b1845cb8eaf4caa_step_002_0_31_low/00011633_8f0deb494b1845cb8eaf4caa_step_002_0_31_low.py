import cadquery as cq

# Parameters
base_plate_width = 80
base_plate_length = 60
base_plate_thickness = 10
base_plate_radius = 20

back_plate_height = 150
back_plate_thickness = 10

block_width = 40
block_length = 50
block_height = 60

top_block_width = 45
top_block_length = 55
top_block_height = 20

pin_radius = 5
pin_length = 15
pin_angle = 30
pin_height_offset = 30

hole_radius = 3
hole_spacing_x_large = 60
hole_spacing_x_small = 40
hole_spacing_y = 50
hole_top_offset = 20

# Base Plate
base_plate = (
    cq.Workplane("XY")
    .rect(base_plate_width, base_plate_length)
    .extrude(base_plate_thickness)
    .edges("|Z")
    .fillet(base_plate_radius)
)

# Back Plate
back_plate = (
    cq.Workplane("XY")
    .transformed(offset=(0, -base_plate_length/2 + back_plate_thickness/2, base_plate_thickness))
    .rect(base_plate_width, back_plate_thickness)
    .extrude(back_plate_height)
)

# Combine plates
result = base_plate.union(back_plate)

# Main Block
block_y_offset = -base_plate_length/2 + back_plate_thickness + block_length/2
main_block = (
    cq.Workplane("XY")
    .transformed(offset=(0, block_y_offset, base_plate_thickness))
    .rect(block_width, block_length)
    .extrude(block_height)
)
result = result.union(main_block)

# Top Block
top_block_y_offset = -base_plate_length/2 + back_plate_thickness + top_block_length/2
top_block = (
    cq.Workplane("XY")
    .transformed(offset=(0, top_block_y_offset, base_plate_thickness + block_height))
    .rect(top_block_width, top_block_length)
    .extrude(top_block_height)
)
result = result.union(top_block)

# Angled Pin
pin_y_offset = block_y_offset + block_length/2
pin_z_offset = base_plate_thickness + pin_height_offset
pin_plane = (
    cq.Workplane("XZ")
    .transformed(offset=(0, pin_z_offset, -pin_y_offset))
    .transformed(rotate=(0, pin_angle, 0))
)
pin = pin_plane.circle(pin_radius).extrude(-pin_length)
result = result.union(pin)

# Holes in back plate
hole_centers = [
    (-hole_spacing_x_large/2, base_plate_thickness + back_plate_height - hole_top_offset),
    (hole_spacing_x_large/2, base_plate_thickness + back_plate_height - hole_top_offset),
    (-hole_spacing_x_small/2, base_plate_thickness + back_plate_height - hole_top_offset - 10),
    (hole_spacing_x_small/2, base_plate_thickness + back_plate_height - hole_top_offset - 10),
    (-hole_spacing_x_large/2, base_plate_thickness + back_plate_height - hole_top_offset - hole_spacing_y),
    (hole_spacing_x_large/2, base_plate_thickness + back_plate_height - hole_top_offset - hole_spacing_y),
    (-hole_spacing_x_small/2, base_plate_thickness + back_plate_height - hole_top_offset - hole_spacing_y - 10),
    (hole_spacing_x_small/2, base_plate_thickness + back_plate_height - hole_top_offset - hole_spacing_y - 10),
]

for center in hole_centers:
    hole = (
        cq.Workplane("XZ")
        .transformed(offset=(center[0], center[1], base_plate_length/2))
        .circle(hole_radius)
        .extrude(-back_plate_thickness*2)
    )
    result = result.cut(hole)
