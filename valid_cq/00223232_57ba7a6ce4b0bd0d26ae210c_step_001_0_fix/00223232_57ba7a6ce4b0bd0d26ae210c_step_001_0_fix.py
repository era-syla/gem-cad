import cadquery as cq

# Base rectangle
base = cq.Workplane("XY").box(40, 25, 5)

# Raised portion
raised = cq.Workplane("XY").workplane(offset=5).rect(20, 25).extrude(10)

# Cylinder
cylinder = cq.Workplane("XY").workplane(offset=15).center(-10, 0).circle(10).extrude(15)

# Fillets on edges
base = base.edges("|Z").fillet(2.5)
raised = raised.edges("|Z").fillet(2.5)

# Combine all parts
result = base.union(raised).union(cylinder)