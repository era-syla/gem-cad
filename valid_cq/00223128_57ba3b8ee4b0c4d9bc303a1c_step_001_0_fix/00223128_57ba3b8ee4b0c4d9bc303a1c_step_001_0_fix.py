import cadquery as cq

# Parameters
d_outer = 30
d_inner = 10
bar_width = 12
thickness = 6
center_dist = 80
fillet_r = 2

# Build end lobes and connecting bar
left_lobe = cq.Workplane("XY").circle(d_outer/2).extrude(thickness).translate((-center_dist/2, 0, 0))
right_lobe = cq.Workplane("XY").circle(d_outer/2).extrude(thickness).translate((center_dist/2, 0, 0))
bar = cq.Workplane("XY").rect(center_dist, bar_width).extrude(thickness)

# Fuse parts
result = left_lobe.union(bar).union(right_lobe)

# Fillet the vertical edges where lobes meet the bar
result = result.edges("|Z").fillet(fillet_r)

# Drill through holes in the lobes
result = result.faces(">Z").workplane().pushPoints([(-center_dist/2, 0), (center_dist/2, 0)]).hole(d_inner, thickness)