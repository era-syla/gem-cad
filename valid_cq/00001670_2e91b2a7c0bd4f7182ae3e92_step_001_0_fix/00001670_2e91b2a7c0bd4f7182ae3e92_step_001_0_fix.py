import cadquery as cq

# Parameters
head_outer_dia = 10.0
head_inner_dia = 6.0
head_height = 2.0
neck_dia = 5.0
neck_length = 2.0
shaft_dia = 4.0
shaft_length = 12.0
slot_width = 4.0
slot_thickness = 1.5
slot_depth = 2.0

# Create screw profile and revolve
result = (
    cq.Workplane("XZ")
    .polyline([
        (0, 0),
        (head_outer_dia/2, 0),
        (head_inner_dia/2, head_height),
        (neck_dia/2, head_height + neck_length),
        (shaft_dia/2, head_height + neck_length + shaft_length),
        (0, head_height + neck_length + shaft_length)
    ])
    .close()
    .revolve()
)

# Cut first slot of the Phillips recess
result = (
    result
    .faces(">Z")
    .workplane()
    .transformed(rotate=(0, 0, 45))
    .rect(slot_width, slot_thickness)
    .cutBlind(slot_depth)
)

# Cut second slot of the Phillips recess
result = (
    result
    .faces(">Z")
    .workplane()
    .transformed(rotate=(0, 0, -45))
    .rect(slot_width, slot_thickness)
    .cutBlind(slot_depth)
)