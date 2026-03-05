import cadquery as cq

# Base block
base = cq.Workplane("XY").box(50, 20, 5)

# Extrusion
extrusion = cq.Workplane("XY").moveTo(0, 10).rect(5, 5).extrude(20)

# Combine
result = base.union(extrusion)