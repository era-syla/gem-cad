import cadquery as cq

# Parameters
span = 80         # distance between hole centers
outer_r = 12      # outer radius of end discs
inner_r = 5       # radius of through holes
thickness = 6     # thickness of the part
bar_w = 8         # width of the connecting bar
fillet_r = 2      # fillet radius on edges

# Create end discs
disc1 = (
    cq.Workplane("XY")
    .center(-span/2, 0)
    .circle(outer_r)
    .extrude(thickness)
)
disc2 = (
    cq.Workplane("XY")
    .center(span/2, 0)
    .circle(outer_r)
    .extrude(thickness)
)

# Create connecting bar
bar = (
    cq.Workplane("XY")
    .rect(span, bar_w)
    .extrude(thickness)
)

# Combine solids
result = disc1.union(disc2).union(bar)

# Cut through holes at ends
hole_positions = [(-span/2, 0), (span/2, 0)]
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .circle(inner_r)
    .cutThruAll()
)

# Fillet all edges
result = result.edges().fillet(fillet_r)