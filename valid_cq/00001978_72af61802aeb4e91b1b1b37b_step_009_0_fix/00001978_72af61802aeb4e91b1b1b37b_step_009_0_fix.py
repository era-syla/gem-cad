import cadquery as cq

# Parameters
plate_thickness = 5
block_width = 40
block_depth = 30
block_height = 60
flange_front_depth = 10
tab_width = 15
tab_depth = 10
hole_d = 6
cyl_d = 30
cyl_h = 15
fillet_r = 3
hole_x = -block_width/2 + 10

# Front flange with hole
plate = (
    cq.Workplane("XY", origin=(0, -flange_front_depth/2, 0))
    .rect(block_width, flange_front_depth)
    .extrude(-plate_thickness)
    .faces(">Z")
    .workplane()
    .pushPoints([(hole_x, 0)])
    .hole(hole_d)
)

# Main block
block = (
    cq.Workplane("XY", origin=(0, 0, plate_thickness))
    .box(block_width, block_depth, block_height, centered=(True, True, False))
)

# Back tab
tab = (
    cq.Workplane("XY", origin=(0, block_depth - tab_depth/2, 0))
    .rect(tab_width, tab_depth)
    .extrude(plate_thickness)
)

# Cylinder under block with filleted bottom edge
cyl = (
    cq.Workplane("XY", origin=(0, block_depth/2, -plate_thickness - cyl_h))
    .circle(cyl_d/2)
    .extrude(cyl_h)
    .faces("<Z")
    .edges()
    .fillet(fillet_r)
)

# Combine all
result = plate.union(block).union(tab).union(cyl)