import cadquery as cq

# Parameters
base_plate_radius = 50
base_plate_thickness = 5
fin_height = 100
fin_width = 80
fin_thickness = 2
mast_length = 150
mast_width = 10
mast_thickness = 10
boom_length = 120
boom_width = 8
boom_thickness = 8
bracket_width = 30
bracket_height = 20
bracket_thickness = 3

# Base Plate
base = cq.Workplane("XY").circle(base_plate_radius).extrude(base_plate_thickness)

# Main Fin (V-shape)
fin = (
    cq.Workplane("YZ")
    .workplane(offset=-fin_thickness/2)
    .moveTo(0, base_plate_thickness)
    .lineTo(fin_width/2, base_plate_thickness + fin_height)
    .lineTo(-fin_width/2, base_plate_thickness + fin_height)
    .close()
    .extrude(fin_thickness)
    .edges("|X")
    .fillet(10)
)

# Vertical Mast
mast = (
    cq.Workplane("XY")
    .workplane(offset=base_plate_thickness)
    .rect(mast_width, mast_thickness)
    .extrude(mast_length)
)

# Horizontal Boom
boom = (
    cq.Workplane("YZ")
    .workplane(offset=-boom_width/2)
    .center(0, base_plate_thickness + 20)
    .rect(boom_length, boom_thickness)
    .extrude(boom_width)
    .translate((0, -boom_length/2 + 20, 0))
)

# Boom Holes
boom = (
    boom.faces(">Z").workplane()
    .rarray(15, 1, 6, 1)
    .circle(2)
    .cutThruAll()
)

# Mounting Brackets
bracket1 = (
    cq.Workplane("XY")
    .workplane(offset=base_plate_thickness)
    .center(20, 0)
    .rect(bracket_thickness, bracket_width)
    .extrude(bracket_height)
    .rotate((0, 0, 0), (0, 1, 0), -30)
)

bracket2 = (
    cq.Workplane("XY")
    .workplane(offset=base_plate_thickness)
    .center(-20, 0)
    .rect(bracket_thickness, bracket_width)
    .extrude(bracket_height)
    .rotate((0, 0, 0), (0, 1, 0), 30)
)

# Combine parts
result = (
    base
    .union(fin)
    .union(mast)
    .union(boom)
    .union(bracket1)
    .union(bracket2)
)
