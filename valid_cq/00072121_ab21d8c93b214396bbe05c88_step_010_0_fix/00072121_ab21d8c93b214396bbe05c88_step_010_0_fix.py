import cadquery as cq

# Parameters
length = 60
width = 25
height = 30
plate_thickness = 3
slot_width = 10
slot_depth = 8
hole_dia = 4
groove_width = 3
groove_depth = 2

# Main slider body
body = cq.Workplane("XY").box(length, width, height)

# Bottom T-slot
body = body.faces("<Z").workplane().rect(length, slot_width).cutBlind(slot_depth)

# Side mounting holes (through X faces)
for y in (10, -10):
    body = body.faces(">X").workplane().center(0, y).hole(hole_dia)
    body = body.faces("<X").workplane().center(0, y).hole(hole_dia)

# Shallow guide grooves on front/back (Y faces)
groove_length = length - 10
body = body.faces(">Y").workplane().rect(groove_length, groove_width).cutBlind(-groove_depth)
body = body.faces("<Y").workplane().rect(groove_length, groove_width).cutBlind(-groove_depth)

# Top clamping plate
plate = cq.Workplane("XY").transformed(offset=(0, 0, height/2 - plate_thickness/2)).box(length, width, plate_thickness)

# Top plate holes
for x in (15, 0, -15):
    plate = plate.faces(">Z").workplane().center(x, 0).hole(hole_dia)

# Combine body and plate
result = body.union(plate)