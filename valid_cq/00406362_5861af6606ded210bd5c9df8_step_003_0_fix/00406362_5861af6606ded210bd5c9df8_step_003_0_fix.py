import cadquery as cq

# Spool parameters
hub_d = 15
hub_l = 20
flange_d = 60
flange_t = 3
bore_d = 8

spool = (
    cq.Workplane("XY")
    .circle(hub_d / 2).extrude(hub_l)
    .faces(">Z").workplane().circle(flange_d / 2).extrude(flange_t)
    .faces("<Z").workplane().circle(flange_d / 2).extrude(flange_t)
    .faces(">Z").workplane().circle(bore_d / 2).cutBlind(flange_t)
    .faces("<Z").workplane().circle(bore_d / 2).cutBlind(flange_t + hub_l)
    .translate((-50, 0, 0))
)

# Bracket plate parameters
plate_w = 30
plate_l = 40
plate_t = 3
cut_s = 10

plate = (
    cq.Workplane("XY")
    .rect(plate_w, plate_l).extrude(plate_t)
    .faces(">Z").workplane().rect(cut_s, cut_s).cutThruAll()
)

# Vertical cylinder on bracket
cyl_d = 15
cyl_h = 40

cylinder = (
    plate.faces(">Z")
    .workplane(centerOption="CenterOfBoundBox")
    .center(-plate_w / 4, 0)
    .circle(cyl_d / 2).extrude(cyl_h)
)

# Horizontal tube on bracket
tube_d = 10
tube_l = 60

tube = (
    plate.faces(">Z")
    .workplane(centerOption="CenterOfBoundBox")
    .center(plate_w / 4, 0)
    .circle(tube_d / 2).extrude(tube_l)
)

result = spool.union(plate).union(cylinder).union(tube)