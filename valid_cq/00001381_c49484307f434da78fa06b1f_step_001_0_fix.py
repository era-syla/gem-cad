import cadquery as cq

# Main plate dimensions
plate_w = 80
plate_h = 55
plate_t = 6

# Central cutout dimensions
cut_w = 42
cut_h = 28

# Corner radius for plate
corner_r = 4

# Mounting boss dimensions
boss_r = 5
boss_h = 4

# Small rectangular slots on sides
slot_w = 6
slot_h = 4

# Create base plate with rounded corners
result = (
    cq.Workplane("XY")
    .rect(plate_w, plate_h)
    .extrude(plate_t)
)

# Round the top edges of the plate
result = result.edges("|Z").fillet(corner_r)
result = result.faces(">Z").edges().fillet(1.0)

# Cut central opening
result = (
    result
    .faces(">Z")
    .workplane()
    .rect(cut_w, cut_h)
    .cutThruAll()
)

# Add raised frame around central cutout
frame_w = cut_w + 10
frame_h = cut_h + 10
frame_thickness = 3

result = (
    result
    .faces(">Z")
    .workplane()
    .rect(frame_w, frame_h)
    .rect(cut_w, cut_h)
    .extrude(frame_thickness)
)

# Add mounting bosses at corners
boss_positions = [
    (-plate_w/2 + 10, -plate_h/2 + 10),
    (plate_w/2 - 10, -plate_h/2 + 10),
    (-plate_w/2 + 10, plate_h/2 - 10),
    (plate_w/2 - 10, plate_h/2 - 10),
]

for pos in boss_positions:
    result = (
        result
        .faces(">Z")
        .workplane()
        .pushPoints([pos])
        .circle(boss_r)
        .extrude(boss_h)
    )

# Add small rectangular slots on the long sides (left and right of frame)
slot_positions = [
    (-frame_w/2 - 1, 0),
    (frame_w/2 + 1, 0),
]

# Cut small rectangular notches on the sides of the frame
for sp in slot_positions:
    result = (
        result
        .faces(">Z")
        .workplane()
        .pushPoints([sp])
        .rect(slot_w, slot_h)
        .cutBlind(-frame_thickness - 1)
    )

# Add screw holes through the bosses
for pos in boss_positions:
    result = (
        result
        .faces(">Z")
        .workplane()
        .pushPoints([pos])
        .circle(2.0)
        .cutThruAll()
    )