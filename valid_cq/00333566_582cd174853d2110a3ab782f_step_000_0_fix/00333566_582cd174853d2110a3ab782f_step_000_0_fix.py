import cadquery as cq

# Parameters
stub_len = 10
stub_dia = 8
left_wt_len = 20
left_wt_dia = 25
rod_len = 60
rod_dia = 8
boss_len = 5
boss_dia = 12
disc_len = 8
disc_dia = 35

# Build geometry by stacking cylinders along the X axis
result = cq.Workplane("YZ").workplane(offset=0).circle(stub_dia/2).extrude(stub_len)
x1 = stub_len
result = result.union(
    cq.Workplane("YZ").workplane(offset=x1).circle(left_wt_dia/2).extrude(left_wt_len)
)
x2 = x1 + left_wt_len
result = result.union(
    cq.Workplane("YZ").workplane(offset=x2).circle(rod_dia/2).extrude(rod_len)
)
x3 = x2 + rod_len
result = result.union(
    cq.Workplane("YZ").workplane(offset=x3).circle(boss_dia/2).extrude(boss_len)
)
x4 = x3 + boss_len
result = result.union(
    cq.Workplane("YZ").workplane(offset=x4).circle(disc_dia/2).extrude(disc_len)
)