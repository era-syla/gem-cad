import cadquery as cq

# Main block dimensions
length = 80
width = 40
height = 30

# Create the main rectangular block
main_block = (
    cq.Workplane("XY")
    .box(length, width, height)
)

# Create horizontal slots on the long sides (front and back)
# These are the grooves visible on the sides
slot_depth = 5
slot_height = 8
slot_width = length + 2  # slightly wider to cut through

# Cut slot on front face (y = +width/2 side)
main_block = (
    main_block
    .faces(">Y")
    .workplane()
    .rect(slot_width, slot_height)
    .cutBlind(slot_depth)
)

# Cut slot on back face (y = -width/2 side)
main_block = (
    main_block
    .faces("<Y")
    .workplane()
    .rect(slot_width, slot_height)
    .cutBlind(slot_depth)
)

# Now cut slots on the left and right short sides
# Vertical slot cuts on left side
slot_side_depth = 5
slot_side_height = 8
slot_side_width = width + 2

# Cut slot on left face
main_block = (
    main_block
    .faces("<X")
    .workplane()
    .rect(slot_side_width, slot_side_height)
    .cutBlind(slot_side_depth)
)

# Cut slot on right face
main_block = (
    main_block
    .faces(">X")
    .workplane()
    .rect(slot_side_width, slot_side_height)
    .cutBlind(slot_side_depth)
)

# Add 3 threaded holes on top face
hole_diameter = 5
hole_depth = 12
hole_spacing = length / 4

main_block = (
    main_block
    .faces(">Z")
    .workplane()
    .pushPoints([
        (-hole_spacing, 0),
        (0, 0),
        (hole_spacing, 0)
    ])
    .hole(hole_diameter, hole_depth)
)

# Add a small hole on the right face (visible in image)
side_hole_dia = 4
main_block = (
    main_block
    .faces(">X")
    .workplane()
    .pushPoints([(0, -2)])
    .hole(side_hole_dia, 8)
)

result = main_block