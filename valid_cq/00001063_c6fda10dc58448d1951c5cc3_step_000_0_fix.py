import cadquery as cq

# Main block dimensions
L = 80  # length (x)
W = 60  # width (y)
H = 25  # height (z)

# Create main rectangular block
result = cq.Workplane("XY").box(L, W, H)

# Create the top cavity (recessed pocket in the top surface)
# Large rectangular pocket in the upper portion
pocket_depth = 12
pocket_L = 60
pocket_W = 40

result = (result
    .faces(">Z")
    .workplane()
    .rect(pocket_L, pocket_W)
    .cutBlind(pocket_depth)
)

# Add the large circular hole/bore in the center of the pocket
bore_radius = 14
result = (result
    .faces(">Z")
    .workplane()
    .circle(bore_radius)
    .cutBlind(H)
)

# Add a smaller rectangular slot through the bore (keyway style)
slot_w = 8
slot_h = 10
result = (result
    .faces(">Z")
    .workplane()
    .rect(slot_w, slot_h)
    .cutBlind(H)
)

# Cut front slot/channel (the slot visible at front-bottom)
front_slot_w = 20
front_slot_h = 12
result = (result
    .faces(">Y")
    .workplane()
    .center(0, H/2 - front_slot_h/2)
    .rect(front_slot_w, front_slot_h)
    .cutBlind(20)
)

# Corner mounting holes - 4 holes on top corners
hole_r = 3
hole_depth = 15
hole_offset_x = 30
hole_offset_y = 20

result = (result
    .faces(">Z")
    .workplane()
    .pushPoints([
        ( hole_offset_x,  hole_offset_y),
        (-hole_offset_x,  hole_offset_y),
        ( hole_offset_x, -hole_offset_y),
        (-hole_offset_x, -hole_offset_y),
    ])
    .circle(hole_r)
    .cutBlind(hole_depth)
)

# Side holes on the right face
side_hole_r = 3
result = (result
    .faces(">X")
    .workplane()
    .pushPoints([
        (0,  10),
        (0, -10),
    ])
    .circle(side_hole_r)
    .cutBlind(10)
)

# Chamfer the bottom edges slightly
result = (result
    .faces("<Z")
    .edges()
    .chamfer(1.5)
)