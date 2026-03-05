import cadquery as cq

# Base block
base = cq.Workplane("XY").box(100, 100, 10)

# Cylinder on the base
cylinder = base.faces(">Z").workplane().circle(20).extrude(50)

# Ring feature
ring = base.faces(">Z").workplane(centerOption="CenterOfBoundBox").circle(50).circle(40).extrude(5)

# Extrusion feature with angles
ext = base.faces(">Z").workplane().circle(30).circle(20, forConstruction=True).vertices().polygon(6, 60).extrude(10)

# Combine all parts
result = base.union(cylinder).union(ring).union(ext)