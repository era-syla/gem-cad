import cadquery as cq

# Parameters
R_end = 10     # Radius of end disks
r_hole = 5     # Radius of through holes
thickness = 4  # Thickness in Z
bar_width = 6  # Width of central bar
center_dist = 40  # Distance between end centers in X
fillet_r = 3   # Fillet radius for smooth transitions

# Create left end disk
left = cq.Workplane("XY") \
    .circle(R_end) \
    .extrude(thickness) \
    .translate((-center_dist/2, 0, 0))

# Create right end disk
right = cq.Workplane("XY") \
    .circle(R_end) \
    .extrude(thickness) \
    .translate(( center_dist/2, 0, 0))

# Create central rectangular bar
bar = cq.Workplane("XY") \
    .rect(center_dist, bar_width) \
    .extrude(thickness)

# Combine solids
result = left.union(bar).union(right)

# Fillet all vertical outer edges
result = result.edges("|Z").fillet(fillet_r)

# Cut through holes at each end
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([(-center_dist/2, 0), (center_dist/2, 0)])
    .circle(r_hole)
    .cutThruAll()
)