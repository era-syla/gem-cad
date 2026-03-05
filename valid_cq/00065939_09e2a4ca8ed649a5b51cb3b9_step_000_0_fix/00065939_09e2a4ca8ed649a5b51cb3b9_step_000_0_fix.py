import cadquery as cq

major_radius = 50
minor_radius = 5

result = cq.Workplane("XZ")\
    .moveTo(major_radius, 0)\
    .circle(minor_radius)\
    .revolve(360)