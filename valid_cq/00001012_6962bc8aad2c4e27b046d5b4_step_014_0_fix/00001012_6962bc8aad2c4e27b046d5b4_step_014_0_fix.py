import cadquery as cq

# Base block
result = cq.Workplane("XY").box(60, 30, 20)

# Split slot (through cut) along X direction
slot_cut = cq.Workplane("XY").box(60, 3, 20)
result = result.cut(slot_cut)

# Cylindrical pocket from top face
result = result.faces(">Z").workplane().circle(15).cutBlind(-15)

# Clamp screw hole through the split (on -X face)
result = result.faces("<X").workplane().pushPoints([(0, 0)]).hole(6)

# Three mounting holes on +X face
mount_points = [(0, -4), (0, 0), (0, 4)]
result = result.faces(">X").workplane().pushPoints(mount_points).hole(4)

# Rectangular boss on top at +X side
result = result.faces(">Z").workplane().transformed(offset=(25, 0, 0)).rect(10, 30).extrude(5)