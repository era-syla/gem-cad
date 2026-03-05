import cadquery as cq

# Parameters
length = 100.0
width = 10.0
thickness = 5.0
hole_dia = 4.0

# Compute straight segment length
straight_length = length - width

# Create main bar body (rectangle + semicircular ends)
bar = cq.Workplane("XY").rect(straight_length, width).extrude(thickness)
end1 = cq.Workplane("XY").center(-straight_length/2, 0).circle(width/2).extrude(thickness)
end2 = cq.Workplane("XY").center(straight_length/2, 0).circle(width/2).extrude(thickness)

result = bar.union(end1).union(end2)

# Drill holes at ends
result = (
    result
    .faces(">Z")
    .workplane()
    .center(-straight_length/2, 0)
    .hole(hole_dia)
    .faces(">Z")
    .workplane()
    .center(straight_length/2, 0)
    .hole(hole_dia)
)