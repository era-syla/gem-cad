import cadquery as cq

# Parameters
profile_size = 20
slot_open = 6
slot_depth = 5
length = 200

# Base extrusion
result = cq.Workplane("XY").rect(profile_size, profile_size).extrude(length)

# Cut slot on +X face
result = result.faces(">X").workplane().rect(slot_depth, slot_open).cutBlind(-slot_depth)

# Cut slot on -X face
result = result.faces("<X").workplane().rect(slot_depth, slot_open).cutBlind(slot_depth)

# Cut slot on +Y face
result = result.faces(">Y").workplane().rect(slot_open, slot_depth).cutBlind(-slot_depth)

# Cut slot on -Y face
result = result.faces("<Y").workplane().rect(slot_open, slot_depth).cutBlind(slot_depth)