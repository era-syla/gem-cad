import cadquery as cq

length = 100
profile_size = 20
slot_width = 6
slot_depth = 5

# Create the base 20x20 profile extruded along Z
result = cq.Workplane("XY").rect(profile_size, profile_size).extrude(length)

# Cut slots into each of the four side faces running the full length
for face in (">X", "<X", ">Y", "<Y"):
    result = (
        result
        .faces(face)
        .workplane()
        .rect(length, slot_width)
        .cutBlind(-slot_depth)
    )