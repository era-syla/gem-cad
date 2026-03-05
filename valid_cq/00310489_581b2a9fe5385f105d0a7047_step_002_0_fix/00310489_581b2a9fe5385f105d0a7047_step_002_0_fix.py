import cadquery as cq
import math

# Parameters
base_w = 20
base_d = 10
height = 80
cap_th = 5
wt = 2
hole_top_d = 8
hole_side_d = 6

# Outer solid including top cap
outer = cq.Workplane("XY").box(base_w, base_d, height + cap_th)

# Subtract interior to form side walls and bottom, leaving front open
inner_w = base_w - 2 * wt
inner_d2 = base_d - wt
inner = (
    cq.Workplane("XY")
    .box(inner_w, inner_d2, height)
    .translate((0, -wt/2, height/2))
)
res = outer.cut(inner)

# Add top hole in cap
res = res.faces(">Z").workplane().hole(hole_top_d)

# Add side holes
res = res.faces(">X").workplane().hole(hole_side_d)
res = res.faces("<X").workplane().hole(hole_side_d)

# Create two simple straight handles rotated about the top pivot
length = 40
width = 6
thickness = 2
z0 = height + cap_th/2 + thickness/2

# A rectangular bar whose one end is at the pivot (origin in XY) at height z0
bar = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .translate((length/2, 0, z0))
)

handle1 = bar.rotate((0, 0, z0), (0, 0, z0 + 1), 45)
handle2 = bar.rotate((0, 0, z0), (0, 0, z0 + 1), -45)

result = res.union(handle1).union(handle2)