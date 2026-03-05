import cadquery as cq
import math

num_teeth = 6
main_radius = 10.0
length = 100.0
groove_radius = 3.0
groove_center_radius = 10.0
bore_diameter = 4.0

# Base cylinder
result = cq.Workplane("XY").circle(main_radius).extrude(length)

# Cut grooves to form lobes
for i in range(num_teeth):
    angle = math.radians(360.0/num_teeth * i)
    x = groove_center_radius * math.cos(angle)
    y = groove_center_radius * math.sin(angle)
    groove = (
        cq.Workplane("XY")
        .center(x, y)
        .circle(groove_radius)
        .extrude(length + 1)  # extra to ensure full cut
    )
    result = result.cut(groove)

# Central bore
result = result.faces(">Z").workplane(centerOption="CenterOfBoundBox").hole(bore_diameter)