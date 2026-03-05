import cadquery as cq

# Parameters
rod_size = 5
rod_height = 200
bar_length = 150
bar_thickness = 10
bar_height = 5
end_radius = bar_thickness/2

# Vertical rod (square cross-section)
rod = (
    cq.Workplane("XY")
    .rect(rod_size, rod_size)
    .extrude(rod_height, both=True)
)

# Horizontal bar with rounded ends
bar = (
    cq.Workplane("XY")
    .center(0, 0)
    .polyline([
        (-bar_length/2 + end_radius, -bar_thickness/2),
        ( bar_length/2 - end_radius, -bar_thickness/2)
    ])
    .threePointArc((bar_length/2, 0), (bar_length/2 - end_radius, bar_thickness/2))
    .lineTo(-bar_length/2 + end_radius, bar_thickness/2)
    .threePointArc((-bar_length/2, 0), (-bar_length/2 + end_radius, -bar_thickness/2))
    .close()
    .extrude(bar_height, both=True)
)

result = rod.union(bar)