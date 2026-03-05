import cadquery as cq

# Base plate
base = cq.Workplane("front").rect(100, 60).extrude(5)

# Add cut for the edge
base = base.faces(">Z").workplane().lineTo(-30, 0).lineTo(-15, -15).lineTo(0, 0).close().cutThruAll()

# Side part
side = cq.Workplane("front").rect(60, 25).extrude(5).translate((25, -32.5, 0))

# Combine base and side
combined = base.union(side)

# Create holes
holes = combined.faces(">Z").workplane().pushPoints([(-30, 20), (-30, -20), (30, 20), (30, -20)])
holes = holes.hole(10)

# Create counterbored holes
counterbore = combined.faces(">Z").workplane().pushPoints([(-30, 0), (30, 0)])
counterbore = counterbore.cboreHole(8, 14, 2)

result = holes.union(counterbore)