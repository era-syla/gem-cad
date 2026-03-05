import cadquery as cq

# Parameters
outer = 40
wall = 3
inner = outer - 2 * wall
fillet_radius = 3
hole_dia = 6
plate_thickness = 3
cut_size = 10

# Bracket body
bracket = cq.Workplane("XY").box(outer, outer, outer)
bracket = bracket.faces("<Y").workplane(offset=wall).rect(inner, inner).cutBlind(inner)
bracket = bracket.edges("|Z").fillet(fillet_radius)
bracket = bracket.faces(">Z").workplane().hole(hole_dia)

# Removable plate
plate = cq.Workplane("XY").box(outer, plate_thickness, outer)
plate = plate.faces(">Y").workplane().rect(cut_size, cut_size).cutBlind(-outer)
plate = plate.translate((0, -outer/2 - plate_thickness/2, 0))

result = bracket.union(plate)