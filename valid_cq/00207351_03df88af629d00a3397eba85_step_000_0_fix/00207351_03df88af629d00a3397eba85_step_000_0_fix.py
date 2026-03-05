import cadquery as cq

# Parameters
block_w = 10
block_d = 10
block_h = 10
cyl_r = 4
cyl_h = 100
hole_d = 4

# Build model
result = (
    cq.Workplane("XY")
    .box(block_w, block_d, block_h)              # rectangular block
    .faces(">Z")                                 # top face of block
    .workplane()                                 # workplane there
    .circle(cyl_r)                               # cylinder profile
    .extrude(cyl_h)                              # extrude cylinder upward
    .faces(">Y")                                 # front face of block
    .workplane()                                 # workplane there
    .hole(hole_d)                                # drill through hole
)