import cadquery as cq

thickness = 3.0
slot_r = 5.0
slot_pitch = 20.0
gap = 10.0

# Left vertical bracket (modeled flat in XY, to be rotated later)
n_left = 4
left_length = slot_pitch*(n_left-1) + 2*slot_r + 10.0
left_width = 30.0
left = (
    cq.Workplane("XY")
    .rect(left_length, left_width)
    .extrude(thickness)
    .faces(">Z")
    .workplane()
    .pushPoints([
        (i*slot_pitch - (n_left-1)*slot_pitch/2, slot_r + 5.0)
        for i in range(n_left)
    ])
    .circle(slot_r)
    .cutBlind(-thickness)
    .translate((
        -( (80.0/2 + left_length/2) + gap ),
        0, 0
    ))
)

# Middle flat plate
plate_size = 80.0
hole_r = 2.0
plate = (
    cq.Workplane("XY")
    .rect(plate_size, plate_size)
    .extrude(thickness)
    .faces(">Z")
    .workplane()
    .pushPoints([
        (-plate_size/2 + 10.0, -plate_size/2 + 10.0),
        ( plate_size/2 - 10.0, -plate_size/2 + 10.0),
        (-plate_size/2 + 10.0,  plate_size/2 - 10.0),
        ( plate_size/2 - 10.0,  plate_size/2 - 10.0),
    ])
    .circle(hole_r)
    .cutBlind(-thickness)
    .faces(">Z")
    .workplane()
    .pushPoints([(-10.0, 0), (10.0, 0)])
    .circle(hole_r)
    .cutBlind(-thickness)
)

# Right horizontal bracket
n_right = 5
right_length = slot_pitch*(n_right-1) + 2*slot_r + 10.0
right_width = 30.0
right = (
    cq.Workplane("XY")
    .rect(right_length, right_width)
    .extrude(thickness)
    .faces(">Z")
    .workplane()
    .pushPoints([
        (i*slot_pitch - (n_right-1)*slot_pitch/2, slot_r + 5.0)
        for i in range(n_right)
    ])
    .circle(slot_r)
    .cutBlind(-thickness)
    .translate((
        (plate_size/2 + right_length/2) + gap,
        0, 0
    ))
)

result = left.union(plate).union(right)