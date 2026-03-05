import cadquery as cq

# Parameters
hub_dia = 20
flange_dia = 40
hub_length = 30
flange_thickness = 5
small_dia = 20
small_height = 10
small_offset = 10

# Build the spool
spool = (
    cq.Workplane("XY")
    .circle(hub_dia/2)
    .extrude(hub_length)
    .faces(">Z")
    .workplane()
    .circle(flange_dia/2)
    .extrude(flange_thickness)
    .faces("<Z")
    .workplane()
    .circle(flange_dia/2)
    .extrude(-flange_thickness)
)

# Build the separate small cylinder
small_cyl = (
    cq.Workplane("XY")
    .circle(small_dia/2)
    .extrude(small_height)
    .translate((0, 0, hub_length + flange_thickness + small_offset))
)

result = spool.union(small_cyl)