import cadquery as cq

# Parameters
profile_size = 20
height = 200
slot_opening_width = 6
slot_opening_depth = 3
slot_undercut_width = 10
slot_undercut_depth = 5

result = cq.Workplane("XY").rect(profile_size, profile_size).extrude(height)

for face_id in (">X", "<X", ">Y", "<Y"):
    result = (
        result.faces(face_id)
              .workplane()
              .rect(slot_opening_width, slot_opening_depth)
              .cutBlind(-slot_opening_depth)
              .workplane(offset=-slot_opening_depth)
              .rect(slot_undercut_width, slot_undercut_depth)
              .cutBlind(-slot_undercut_depth)
    )