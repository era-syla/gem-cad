import cadquery as cq

# Parameters
thickness = 2.0
width_left = 60.0
height_left = 80.0
width_right = 70.0
height_right = 100.0

total_width = width_left + width_right

# Base plate (combining two rectangles)
pts = [
    (0, 0),
    (width_left, 0),
    (width_left, - (height_right - height_left)),
    (total_width, - (height_right - height_left)),
    (total_width, height_left),
    (0, height_left),
]

result = (
    cq.Workplane("XY")
    .polyline(pts).close()
    .extrude(thickness)
)

# Left cutout
cutout_w = 45
cutout_h = 25
result = (
    result.faces(">Z").workplane()
    .center(width_left/2, height_left/2 + 10)
    .rect(cutout_w, cutout_h)
    .cutThruAll()
)

# Vent slots left
slot_w = 3
slot_h = 25
slot_pitch = 8
for i in range(5):
    result = (
        result.faces(">Z").workplane()
        .center(10 + i * slot_pitch, 20)
        .slot2D(slot_h, slot_w)
        .cutThruAll()
    )

# Vent slots right
for i in range(5):
    result = (
        result.faces(">Z").workplane()
        .center(width_left + 15 + i * slot_pitch, 20 - (height_right - height_left)/2)
        .slot2D(slot_h, slot_w)
        .cutThruAll()
    )

# Small square cutouts right
result = (
    result.faces(">Z").workplane()
    .center(width_left + 25, height_left - 15)
    .rect(8, 12)
    .cutThruAll()
)

result = (
    result.faces(">Z").workplane()
    .center(width_left + 45, height_left - 10)
    .rect(6, 6)
    .cutThruAll()
)

# Mounting holes
hole_radius = 1.5
hole_pts = [
    (3, 3), (width_left-3, 3), (3, height_left-3), (width_left-3, height_left-3),
    (width_left+3, -(height_right-height_left)+3), (total_width-3, -(height_right-height_left)+3),
    (width_left+3, height_left-3), (total_width-3, height_left-3),
    (total_width-3, height_left/2)
]

result = (
    result.faces(">Z").workplane()
    .pushPoints(hole_pts)
    .hole(hole_radius * 2)
)

# Fillets
result = result.edges("|Z").fillet(2.0)