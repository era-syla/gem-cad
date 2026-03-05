import cadquery as cq

D_body = 30
L_body = 60
D_collar = 35
L_collar = 5
D_rod = 15
L_rod = 40
lug_plate_th = 3
lug_plate_height = 20
lug_half_dist = 8
holeD = 6
outer_eye_D = 18
ring_th = 4

# main cylinder body along X
result = cq.Workplane("YZ").circle(D_body/2).extrude(L_body)

# collar at mid-length
collar = cq.Workplane("YZ").circle(D_collar/2).extrude(L_collar).translate((L_body/2 - L_collar/2, 0, 0))
result = result.union(collar)

# rod extension
rod = cq.Workplane("YZ").circle(D_rod/2).extrude(L_rod).translate((L_body, 0, 0))
result = result.union(rod)

# clevis lugs at the left end
lugs = cq.Workplane("YZ").workplane(offset=0).pushPoints([(0, lug_half_dist), (0, -lug_half_dist)]).rect(lug_plate_th, lug_plate_height).extrude(-lug_plate_th)
result = result.union(lugs)

# cut pin holes through the lugs (axis along Y)
hole_cuts = cq.Workplane("XZ").pushPoints([(-lug_plate_th/2, lug_half_dist), (-lug_plate_th/2, -lug_half_dist)]).circle(holeD/2).extrude(2*D_body)
result = result.cut(hole_cuts)

# eye ring at the rod tip
eye = cq.Workplane("YZ").circle(outer_eye_D/2).circle(holeD/2).extrude(ring_th).translate((L_body + L_rod, 0, 0))
result = result.union(eye)