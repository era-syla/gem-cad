import cadquery as cq

# Base part
base = cq.Workplane("XY").box(20, 60, 10)

# L-shaped bracket
bracket = (
    cq.Workplane("XY")
    .lineTo(10, 0)
    .lineTo(10, 40)
    .lineTo(20, 50)
    .lineTo(0, 50)
    .close()
    .extrude(10)
)

# Combine base and bracket
combined = base.union(bracket)

# Front face features
front_face = (
    combined.faces(">Y")
    .workplane(centerOption="CenterOfBoundBox")
    .rect(20, 20)
    .extrude(5)
)

# Top holes
top_holes = (
    combined.faces(">Z")
    .workplane(centerOption="CenterOfBoundBox")
    .circle(5).cutThruAll()
    .rarray(15, 15, 3, 3)
    .circle(2).cutThruAll()
)

# Final result
result = combined.union(front_face).cut(top_holes)