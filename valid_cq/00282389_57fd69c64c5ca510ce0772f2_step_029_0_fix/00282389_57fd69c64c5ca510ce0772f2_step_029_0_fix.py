import cadquery as cq

# Parameters
profile_size = 20.0
length = 200.0
slot_width = 6.0
slot_depth = 5.0

# Create the basic extrusion
result = cq.Workplane("XY").box(profile_size, profile_size, length)

# Cut T‐slot style grooves on each face
result = result.faces(">X").workplane().rect(slot_width, length).cutBlind(-slot_depth)
result = result.faces("<X").workplane().rect(slot_width, length).cutBlind(-slot_depth)
result = result.faces(">Y").workplane().rect(slot_width, length).cutBlind(-slot_depth)
result = result.faces("<Y").workplane().rect(slot_width, length).cutBlind(-slot_depth)