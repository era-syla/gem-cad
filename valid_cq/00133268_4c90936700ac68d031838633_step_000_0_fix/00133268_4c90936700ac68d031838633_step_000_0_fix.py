import cadquery as cq

# Parameters
outer_dia = 100
thickness = 8
height = 10
gap = 3
lug_len = 20
lug_w = thickness
hole_dia = 5

inner_dia = outer_dia - 2*thickness
inner_r = inner_dia/2
outer_r = outer_dia/2

# Ring
result = cq.Workplane("XY").circle(outer_r).circle(inner_r).extrude(height)

# Cut the gap at the top
gap_cut = cq.Workplane("XY").box(outer_dia, gap, height + 1).translate((0, outer_r - gap/2, height/2))
result = result.cut(gap_cut)

# Add side lugs
lug = cq.Workplane("XY").box(lug_len, lug_w, height)
lug1 = lug.translate((outer_r + lug_len/2, 0, height/2))
lug2 = lug.translate((-outer_r - lug_len/2, 0, height/2))
result = result.union(lug1).union(lug2)

# Add triangular gussets on inside
tri = (
    cq.Workplane("XY")
    .polyline([(inner_r, lug_w/2), (inner_r, -lug_w/2), (outer_r + lug_len, 0)])
    .close()
    .extrude(height)
)
gusset1 = tri
gusset2 = tri.mirror(mirrorPlane="YZ", union=False)
result = result.union(gusset1).union(gusset2)

# Drill bolt holes through the lugs
hole_pts = [(outer_r + lug_len/2, 0), (-outer_r - lug_len/2, 0)]
result = result.faces(">Z").workplane().pushPoints(hole_pts).hole(hole_dia)