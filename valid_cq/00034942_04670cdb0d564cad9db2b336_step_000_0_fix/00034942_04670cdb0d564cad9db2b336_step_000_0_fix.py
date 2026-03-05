import cadquery as cq

length = 120.0
width = 12.0
thickness = 2.0
end_offset = 5.0
hole_diameter = 4.0
hole_count = 7
spacing = 8.0

points = [(0, -length/2 + end_offset)]
for i in range(hole_count):
    y = length/2 - end_offset - i * spacing
    points.append((0, y))

result = (
    cq.Workplane("XY")
    .rect(width, length)
    .extrude(thickness)
    .faces(">Z")
    .workplane()
    .pushPoints(points)
    .hole(hole_diameter)
)