import cadquery as cq

# Main dimensions
total_length = 80
front_tube_length = 50
front_tube_od = 28
front_tube_id = 10

collar_length = 12
collar_od = 42
collar_id = front_tube_od

rear_length = 20
rear_od = 38
rear_id = front_tube_od

# Build the part along X axis
# Front tube
result = (
    cq.Workplane("YZ")
    .circle(front_tube_od / 2)
    .extrude(front_tube_length)
)

# Collar/flange
result = (
    result
    .faces(">X")
    .workplane()
    .circle(collar_od / 2)
    .extrude(collar_length)
)

# Rear cylinder
result = (
    result
    .faces(">X")
    .workplane()
    .circle(rear_od / 2)
    .extrude(rear_length)
)

# Hollow out the center bore through entire part
result = (
    result
    .faces("<X")
    .workplane()
    .circle(front_tube_id / 2)
    .cutThruAll()
)

# Add groove/channel on front tube - two slots cut into the front tube
slot_width = 4
slot_depth = 5
slot_length = 25

# Cut two opposing slots into the front tube (top and bottom)
result = (
    result
    .workplane(offset=front_tube_length - slot_length, origin=(0, 0, 0))
    .center(0, 0)
    .rect(slot_width, front_tube_od + 2)
    .cutBlind(-slot_length)
)

# Second slot perpendicular
result = (
    result
    .workplane(offset=0, origin=(0, 0, 0))
    .transformed(rotate=(0, 0, 90))
    .center(0, 0)
    .rect(slot_width, front_tube_od + 2)
    .cutBlind(-slot_length)
)

# Add a small hole in the collar (set screw hole)
result = (
    result
    .faces(">X[-2]")
    .workplane()
    .center(0, collar_od / 2 - 4)
    .circle(1.5)
    .cutBlind(-8)
)

# Add a chamfer at front face
result = (
    result
    .faces("<X")
    .edges()
    .chamfer(1.5)
)

# Add small fillet at collar transitions
result = (
    result
    .faces(">X[-1]")
    .edges("<X")
    .fillet(1.0)
)