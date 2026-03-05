import cadquery as cq

# Parameters
thickness = 4.0
length = 80.0
width = 30.0
end_radius = width / 2.0
small_hole_dia = 5.0
center_hole_dia = 10.0

# Create center rectangle
center_rect = cq.Workplane("XY").rect(length - 2 * end_radius, width).extrude(thickness)

# Create end caps
end_cap = cq.Workplane("XY").circle(end_radius).extrude(thickness)
left_cap = end_cap.translate((-length/2 + end_radius, 0, 0))
right_cap = end_cap.translate(( length/2 - end_radius, 0, 0))

# Combine all parts
result = center_rect.union(left_cap).union(right_cap)

# Drill holes
hole_positions = [(-length/2 + end_radius, 0), ( length/2 - end_radius, 0)]
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(small_hole_dia)
    .pushPoints([(0, 0)])
    .hole(center_hole_dia)
)