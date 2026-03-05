import cadquery as cq

# Main cylinder body
result = cq.Workplane("XY").circle(10).extrude(60)

# Front cap
result = result.faces(">Z").workplane().circle(12).extrude(5)

# Rear cap
result = result.faces("<Z").workplane().circle(12).extrude(-5)

# Connecting pin front
result = result.faces(">Z").workplane(centerOption="ProjectedOrigin").center(0, -12).circle(3).extrude(-4)

# Connecting pin rear
result = result.faces("<Z").workplane(centerOption="ProjectedOrigin").center(0, -12).circle(3).extrude(4)

# Piston rod
result = result.faces(">Z[1]").workplane(centerOption="ProjectedOrigin").circle(5).extrude(50)

# Nuts on the back
result = result.faces("<Z[1]").workplane(centerOption="ProjectedOrigin").center(0, 10).polygon(6, 8).extrude(-2)