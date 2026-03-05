import cadquery as cq

plate_thk = 8
plate_y = 60
plate_z = 120

pocket_z = 25
pocket_y = 20
pocket_depth = 4
rib = (plate_z - 4 * pocket_z) / 5

zs = [
    -plate_z / 2 + rib + pocket_z / 2 + i * (pocket_z + rib)
    for i in range(4)
]

res = cq.Workplane("XY").box(plate_thk, plate_y, plate_z, centered=(True, True, True))
res = res.faces(">X").workplane().pushPoints([(0, z) for z in zs]).rect(pocket_z, pocket_y).cutBlind(pocket_depth)

flange_radius = 12
flange_thk = 6
tube_radius = 5
tube_length = 80
y_offset = -15
tube_zs = [-12, 12]

for z in tube_zs:
    flange = (
        cq.Workplane("YZ", origin=(plate_thk / 2, y_offset, z))
        .circle(flange_radius)
        .extrude(flange_thk)
    )
    tube = (
        cq.Workplane("YZ", origin=(plate_thk / 2 + flange_thk, y_offset, z))
        .circle(tube_radius)
        .extrude(tube_length)
    )
    res = res.union(flange).union(tube)

screw_radius = 4
screw_length = 10
res = res.faces("<X").workplane().circle(screw_radius).extrude(-screw_length)

result = res