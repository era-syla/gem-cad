import cadquery as cq
import math

# Parameters
length = 200
od = 40
wall = 2
id = od - 2*wall
flange_od = 50
flange_th = 5
branch_od = 12
branch_wall = 1.5
branch_len = 30
branch_angle_deg = 45
branch_x = length * 0.6
R = od/2

# Main hollow cylinder
outer = cq.Workplane("YZ").circle(od/2).extrude(length)
inner = cq.Workplane("YZ").circle(id/2).extrude(length + 2*wall).translate((0, 0, -wall))
body = outer.cut(inner)

# End flanges
cap1 = cq.Workplane("YZ").workplane(origin=(0, 0, 0)).circle(flange_od/2).extrude(flange_th)
cap2 = cq.Workplane("YZ").workplane(origin=(0, 0, length)).circle(flange_od/2).extrude(-flange_th)

# Branch pipe
branch_outer = cq.Workplane("XY").circle(branch_od/2).extrude(branch_len)
branch_inner = (
    cq.Workplane("XY")
    .circle((branch_od - 2*branch_wall)/2)
    .extrude(branch_len + 4)
    .translate((0, 0, -2))
)
branch = (
    branch_outer
    .cut(branch_inner)
    .rotate((0, 0, 0), (1, 0, 0), branch_angle_deg)
    .translate((branch_x, R / math.sqrt(2), R / math.sqrt(2)))
)

result = body.union(cap1).union(cap2).union(branch)