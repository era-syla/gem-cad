import cadquery as cq

# Parameters
block_len = 30
center_len = 20
block_w = 20
center_w = 12
base_h = 8
plate_h = 2
groove_w = 2
groove_d = 1

# Build base blocks
left = cq.Workplane("XY").box(block_len, block_w, base_h, centered=(True,True,False)).translate((-(center_len/2+block_len/2), 0, 0))
center = cq.Workplane("XY").box(center_len, center_w, base_h, centered=(True,True,False))
right = cq.Workplane("XY").box(block_len, block_w, base_h, centered=(True,True,False)).translate((center_len/2+block_len/2, 0, 0))
result = left.union(center).union(right)

# Grooves on top of center bar
for y in (-4, 4):
    result = result.faces(">Z").workplane(offset=base_h).transformed(offset=(0, y, 0)).rect(center_len-2, groove_w).cutBlind(-groove_d)

# Top plate on center bar
plate = cq.Workplane("XY").box(center_len, center_w, plate_h, centered=(True,True,False)).translate((0, 0, base_h))
result = result.union(plate)

# Extrude letter "B" on plate
result = result.faces(">Z").workplane(offset=base_h).text("B", 10, plate_h, combine=True)

# Top holes in end blocks
for x in (-(center_len/2+block_len/2), center_len/2+block_len/2):
    result = result.faces(">Z").workplane(offset=base_h).transformed(offset=(x, 0, 0)).hole(5)

# Side holes on left and right ends
result = result.faces("<X").workplane().hole(3)
result = result.faces(">X").workplane().hole(3)