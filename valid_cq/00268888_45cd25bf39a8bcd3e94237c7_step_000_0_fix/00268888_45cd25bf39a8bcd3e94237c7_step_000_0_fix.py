import cadquery as cq

result = (
    cq.Workplane("XY")
    .circle(5).extrude(50)           # Shaft: 10 mm dia, 50 mm length
    .workplane(offset=50)
    .circle(7.5).extrude(5)         # Shoulder: 15 mm dia, 5 mm length
    .workplane(offset=5)
    .circle(12.5).extrude(5)        # Head: 25 mm dia, 5 mm length
)