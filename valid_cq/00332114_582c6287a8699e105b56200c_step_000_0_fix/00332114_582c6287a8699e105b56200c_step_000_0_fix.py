import cadquery as cq

# Parameters
rod_d = 20.0
rod_l = 80.0
disc_d = 30.0
disc_t = 5.0
block_w = 12.0
block_d = 8.0
block_h = 6.0
hole_d = 4.0

offsetY = disc_d/2 - block_d/2

result = (
    cq.Workplane("XY")
    # main rod
    .circle(rod_d/2).extrude(rod_l)
    # top disc
    .faces(">Z").workplane().circle(disc_d/2).extrude(disc_t)
    # top block
    .faces(">Z").workplane().center(0, offsetY).rect(block_w, block_d).extrude(block_h)
    # top hole
    .faces(">Z").workplane().circle(hole_d/2).cutThruAll()
    # bottom disc
    .faces("<Z").workplane().circle(disc_d/2).extrude(-disc_t)
    # bottom block
    .faces("<Z").workplane().center(0, -offsetY).rect(block_w, block_d).extrude(-block_h)
    # bottom hole
    .faces("<Z").workplane().circle(hole_d/2).cutThruAll()
)
