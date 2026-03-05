import cadquery as cq

# Parameters
cap_length = 5
cap_d = 12
collar_th = 2
collar_d = 15
tube_length = 60
tube_d = 10
block_length = 12   # along X
block_width = 15    # along Y
block_height = 8    # along Z
lug_z = 4           # lug thickness in Z
lug_y = 6           # lug thickness in Y (hole clearance)
hole_d = 4
clamp_th = 2
clamp_w = 6
pin_d = 3
hole_extra = 5

# Build cap
cap = cq.Workplane("YZ").circle(cap_d/2).extrude(cap_length)

# Build collar
collar = cap.faces(">X").workplane().circle(collar_d/2).extrude(collar_th)

# Build tube
tube = collar.faces(">X").workplane().circle(tube_d/2).extrude(tube_length)

# Compute positions
tube_end_x = cap_length + collar_th + tube_length
block_center_x = tube_end_x + block_length/2

# Build block
block = cq.Workplane("XY").box(block_length, block_width, block_height)
block = block.translate((block_center_x, 0, 0))

# Build top lug
lug_top = cq.Workplane("XY").box(block_length, lug_y, lug_z)
lug_top = lug_top.translate((block_center_x, 0, block_height/2 + lug_z/2))

# Build bottom lug
lug_bottom = cq.Workplane("XY").box(block_length, lug_y, lug_z)
lug_bottom = lug_bottom.translate((block_center_x, 0, -(block_height/2 + lug_z/2)))

# Combine tube, block, and lugs
assembly = tube.union(block).union(lug_top).union(lug_bottom)

# Cut holes through lugs and block
hole_cut = (
    cq.Workplane("XZ")
    .transformed(offset=(block_center_x, -block_width/2 - hole_extra, 0))
    .circle(hole_d/2)
    .extrude(block_width + 2 * hole_extra)
)
assembly = assembly.cut(hole_cut)

# Build clamp ring around tube
ring = (
    cq.Workplane("YZ")
    .transformed(offset=(cap_length + collar_th + tube_length, 0, 0))
    .circle(tube_d/2 + clamp_th)
    .circle(tube_d/2)
    .extrude(clamp_w)
)
assembly = assembly.union(ring)

# Build pin through lugs
pin = (
    cq.Workplane("XZ")
    .transformed(offset=(block_center_x, -block_width/2 - hole_extra, 0))
    .circle(pin_d/2)
    .extrude(block_width + 2 * hole_extra)
)
assembly = assembly.union(pin)

result = assembly	
