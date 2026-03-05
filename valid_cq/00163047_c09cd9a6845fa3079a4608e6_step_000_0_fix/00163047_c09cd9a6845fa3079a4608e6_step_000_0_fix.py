import cadquery as cq

outer_diameter = 100
inner_diameter = 50
thickness = 5
hole_diameter = 5
holes_positions = [(20, 20), (-20, 20), (20, -20), (-20, -20)]

result = (cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .circle(inner_diameter / 2)
    .extrude(thickness)
    .faces(">Z")
    .workplane()
    .pushPoints(holes_positions)
    .hole(hole_diameter)
)