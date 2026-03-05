import cadquery as cq

length = 500.0
width_center = 100.0
width_end = 60.0
thickness = 6.0
end_radius = 50.0

half_straight = (length - 2 * end_radius) / 2.0

p1 = (half_straight,  width_center/2)
p2 = (half_straight + end_radius,  width_end/2)
p3 = (half_straight + end_radius, -width_end/2)
p4 = (half_straight, -width_center/2)
p5 = (-half_straight, -width_center/2)
p6 = (-half_straight - end_radius, -width_end/2)
p7 = (-half_straight - end_radius,  width_end/2)
p8 = (-half_straight,  width_center/2)

outline = [p1, p2, p3, p4, p5, p6, p7, p8]

# hole pattern: clusters at both ends and center
cluster_centers = [
    -(half_straight + end_radius - 10),
     0.0,
     (half_straight + end_radius - 10)
]
inner_offsets_x = [-10, 10]
inner_offsets_y = [-15, 15]
hole_points = [
    (cx + ix, iy)
    for cx in cluster_centers
    for ix in inner_offsets_x
    for iy in inner_offsets_y
]

result = (
    cq.Workplane("XY")
      .polyline(outline)
      .close()
      .extrude(thickness)
      .edges("|Z")
      .fillet(5)
      .faces(">Z")
      .workplane()
      .pushPoints(hole_points)
      .hole(5.0)
)