import cadquery as cq

bar_count = 5
bar_width = 1.0
bar_depth = 1.0
bar_height = 100.0
spacing = 2.0

offset = (bar_count - 1) / 2 * spacing
points = [((i * spacing) - offset, 0) for i in range(bar_count)]

result = (
    cq.Workplane("XY")
    .pushPoints(points)
    .rect(bar_width, bar_depth)
    .extrude(bar_height)
)