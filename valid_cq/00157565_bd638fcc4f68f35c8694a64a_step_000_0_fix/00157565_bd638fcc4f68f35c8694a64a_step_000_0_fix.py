import cadquery as cq

# Main body
base = cq.Workplane("XY").box(200, 40, 20)

# Cylindrical housing at the rear
cyl = base.faces("<X").workplane().circle(30).extrude(40)

# Top rail
rail = (base.union(cyl)
    .faces("+Z").workplane()
    .rect(180, 20).extrude(5)
)

# Handle/profile extruded downward
handle = (cq.Workplane("YZ", origin=(60, 0, 10))
    .polyline([(0, 0), (0, -40), (10, -60), (14, -60), (14, -5)])
    .close()
    .extrude(-20)
)

# Combine all parts
result = base.union(cyl).union(rail).union(handle)