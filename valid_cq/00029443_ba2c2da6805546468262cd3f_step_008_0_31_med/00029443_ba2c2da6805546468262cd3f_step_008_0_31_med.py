import cadquery as cq

# Parameters
num_holes = 30
pitch = 12.7
width = 12.7
thickness = 1.6
hole_dia = 4.5
length = num_holes * pitch

# Create the base L-bracket profile on the YZ plane and extrude along X
profile = (
    cq.Workplane("YZ")
    .moveTo(0, 0)
    .lineTo(width, 0)
    .lineTo(width, thickness)
    .lineTo(thickness, thickness)
    .lineTo(thickness, width)
    .lineTo(0, width)
    .close()
)

result = profile.extrude(length)

# Calculate hole center coordinates
x_pts = [(i + 0.5) * pitch for i in range(num_holes)]
center_offset = thickness + (width - thickness) / 2

# Cut holes in the horizontal leg (normal to Z)
pts_h = [(x, center_offset) for x in x_pts]
wp_h = cq.Workplane("XY", origin=(0, 0, -thickness))
result = result.cut(
    wp_h.pushPoints(pts_h)
    .circle(hole_dia / 2)
    .extrude(thickness * 4)
)

# Cut holes in the vertical leg (normal to Y)
pts_v = [(x, center_offset) for x in x_pts]
wp_v = cq.Workplane("XZ", origin=(0, -thickness, 0))
result = result.cut(
    wp_v.pushPoints(pts_v)
    .circle(hole_dia / 2)
    .extrude(thickness * 4)
)

# Apply a small fillet to smooth sharp outer edges
result = result.edges(">X or <X").fillet(0.5)