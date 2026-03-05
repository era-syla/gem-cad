import cadquery as cq

length = 100.0
width = 5.0
height = 5.0
thickness = 1.0
hole_diameter = 1.5
hole_spacing = 5.0

bar = cq.Workplane("XY").box(length, width, thickness)
holes = bar.faces(">Z").workplane().rarray(hole_spacing, hole_spacing, int(length / hole_spacing), 1).circle(hole_diameter / 2).cutThruAll()

bracket = cq.Workplane("XZ").box(width, thickness, height).translate((0, -width / 2, height / 2))
bracket = bracket.faces(">Y").workplane().hole(hole_diameter)

result = holes.union(bracket.translate((-length / 2, 0, thickness / 2)))