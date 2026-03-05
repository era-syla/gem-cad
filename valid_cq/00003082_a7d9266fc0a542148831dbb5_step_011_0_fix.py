import cadquery as cq

# Hex nut parameters
across_flats = 13.0  # M8 hex nut across flats
height = 6.5         # nut height
hole_dia = 6.8       # inner hole diameter (M8 thread minor dia approx)
chamfer_top = 1.0    # chamfer on top/bottom edges

# Compute circumscribed circle diameter for polygon
# across_flats = diameter * cos(30) => diameter = across_flats / cos(30)
import math
hex_diameter = across_flats / math.cos(math.radians(30))

# Create hex body
hex_body = (
    cq.Workplane("XY")
    .polygon(6, hex_diameter)
    .extrude(height)
)

# Chamfer top and bottom edges of hex
# Select top and bottom edges (horizontal edges)
hex_body = (
    hex_body
    .faces(">Z")
    .edges()
    .chamfer(chamfer_top)
)

hex_body = (
    hex_body
    .faces("<Z")
    .edges()
    .chamfer(chamfer_top * 0.7)
)

# Cut the center hole (threaded hole approximation - smooth cylinder)
hex_body = (
    hex_body
    .faces(">Z")
    .workplane()
    .circle(hole_dia / 2)
    .cutThruAll()
)

# Add countersink-like chamfer on top of hole (bearing surface)
# We create a conical chamfer by cutting a cone shape from top
cone_outer = hole_dia / 2 + 1.5
cone_inner = hole_dia / 2

chamfer_depth = 1.2

cone_cut = (
    cq.Workplane("XY")
    .workplane(offset=height)
    .add(
        cq.Solid.makeCone(cone_outer, cone_inner, chamfer_depth,
                          pnt=cq.Vector(0, 0, height - chamfer_depth),
                          dir=cq.Vector(0, 0, 1))
    )
)

hex_body = hex_body.cut(cone_cut)

result = hex_body