import cadquery as cq

# Parameters
end_r = 12.5       # radius of end circles
hole_d = 8         # hole diameter
bar_len = 80       # distance between the centers of the end circles
bar_w = 12         # width of the rectangular bar
thk = 6            # thickness (extrusion height)
fillet_r = 2       # fillet radius

# Create left end cylinder
cyl1 = cq.Workplane("XY").center(-bar_len/2, 0).circle(end_r).extrude(thk)

# Create right end cylinder
cyl2 = cq.Workplane("XY").center(bar_len/2, 0).circle(end_r).extrude(thk)

# Create connecting rectangular bar
rect = cq.Workplane("XY").rect(bar_len, bar_w).extrude(thk)

# Combine the three solids
result = cyl1.union(cyl2).union(rect)

# Apply fillets to all edges
result = result.edges().fillet(fillet_r)

# Drill through holes at each end
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([(-bar_len/2, 0), (bar_len/2, 0)])
    .hole(hole_d, thk)
)