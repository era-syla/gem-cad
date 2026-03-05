import cadquery as cq

# Parameters for the CSG text block
size = 100.0
font_name = "Arial"
font_kind = "bold"

# Create the three extruded texts, centering the extrusions at the origin
# Top face reads 'S'
s = cq.Workplane("XY").workplane(offset=-size/2.0).text(
    "S", size, size, font=font_name, kind=font_kind, halign="center", valign="center"
)

# Front-left face reads 'C' (XZ plane normal is -Y, viewed from -Y)
c = cq.Workplane("XZ").workplane(offset=-size/2.0).text(
    "C", size, size, font=font_name, kind=font_kind, halign="center", valign="center"
)

# Front-right face reads 'G' (YZ plane normal is +X, viewed from +X)
g = cq.Workplane("YZ").workplane(offset=-size/2.0).text(
    "G", size, size, font=font_name, kind=font_kind, halign="center", valign="center"
)

# Constructive Solid Geometry intersection to form the final block
result = s.intersect(c).intersect(g)