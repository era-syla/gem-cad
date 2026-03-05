import cadquery as cq

# Parameters
r_small = 5.0
r_large = 25.0
flange_thickness = 2.0
height = 100.0

# Create bottom flange
flange = cq.Workplane("XY").circle(r_small).extrude(flange_thickness)

# Create tapered section by lofting from small circle to large circle
taper = (
    flange.faces(">Z")
    .workplane()
    .circle(r_small)
    .workplane(offset=height)
    .circle(r_large)
    .loft()
)

# Combine flange and tapered section into final result
result = flange.union(taper)