import cadquery as cq

# Main plate dimensions
plate_size = 100
plate_thickness = 4
corner_radius = 15

# Create the main square plate with rounded corners
result = (
    cq.Workplane("XY")
    .rect(plate_size, plate_size)
    .extrude(plate_thickness)
)

# Round the top edges corners
result = (
    result
    .edges("|Z")
    .fillet(corner_radius)
)

# Round top and bottom face edges slightly
result = (
    result
    .edges("#Z")
    .fillet(1.0)
)

# Center hole
result = (
    result
    .faces(">Z")
    .workplane()
    .hole(10)
)

# Create slots - there are 4 slots arranged in a cross pattern (rotated 45 degrees in appearance)
# But looking at the image, they appear to be horizontal/vertical slots near the edges
# Two horizontal slots and two vertical slots

slot_length = 50
slot_width = 6
slot_depth = plate_thickness
slot_offset = 28

# Horizontal slots (left and right areas)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(-slot_offset, 0)
    .slot2D(slot_length, slot_width, 90)
    .cutThruAll()
)

result = (
    result
    .faces(">Z")
    .workplane()
    .center(slot_offset, 0)
    .slot2D(slot_length, slot_width, 90)
    .cutThruAll()
)

# Vertical slots (top and bottom areas)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, slot_offset)
    .slot2D(slot_length, slot_width, 0)
    .cutThruAll()
)

result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, -slot_offset)
    .slot2D(slot_length, slot_width, 0)
    .cutThruAll()
)

# Add corner arc features - small rounded rectangular cutouts at corners
# These appear as C-shaped or bracket features at the corners
corner_pos = 32
arc_outer = 14
arc_inner = 8
arc_depth = plate_thickness

# Corner bracket cutouts - create C-shaped slots at each corner
# Using slot2D at 45-degree positions
corner_positions = [
    (corner_pos, corner_pos, 45),
    (-corner_pos, corner_pos, -45),
    (-corner_pos, -corner_pos, 45),
    (corner_pos, -corner_pos, -45),
]

for cx, cy, angle in corner_positions:
    result = (
        result
        .faces(">Z")
        .workplane()
        .center(cx, cy)
        .slot2D(18, 5, angle)
        .cutThruAll()
    )

# Add small raised rim/border effect - add a thin lip around the inner square area
# This represents the raised grid pattern visible in the image
# Create inner depression
inner_size = 70
depression_depth = 1.5

result = (
    result
    .faces(">Z")
    .workplane()
    .rect(inner_size, inner_size)
    .cutBlind(-depression_depth)
)

# Add small dots pattern (visible in the image as a row of dots on bottom slot area)
# These are small circular indentations
dot_radius = 1.0
dot_depth = 0.5
dot_spacing = 5
num_dots = 5

for i in range(num_dots):
    dx = (i - (num_dots - 1) / 2.0) * dot_spacing
    result = (
        result
        .faces(">Z")
        .workplane()
        .center(dx, -slot_offset)
        .circle(dot_radius)
        .cutBlind(-dot_depth)
    )