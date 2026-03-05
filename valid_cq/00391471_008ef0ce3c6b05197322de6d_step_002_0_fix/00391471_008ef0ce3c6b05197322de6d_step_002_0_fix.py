import cadquery as cq

length = 200.0
profile_size = 20.0
slot_width = 6.0
slot_depth = 4.0

result = cq.Workplane("XY").rect(profile_size, profile_size).extrude(length)
for face in [">X", "<X", ">Y", "<Y"]:
    result = result.faces(face).workplane().rect(slot_width, slot_depth).cutBlind(slot_depth)