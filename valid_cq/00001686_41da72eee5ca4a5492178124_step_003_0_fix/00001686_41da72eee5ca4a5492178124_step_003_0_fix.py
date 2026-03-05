import cadquery as cq

# Parameters
width = 100.0
height = 60.0
depth = 20.0

side_thickness = 5.0
rib_thickness = 2.0
panel_depth = 2.0

band_height = 6.0
band_depth = 3.0

# Derived dimensions
panel_width = (width - 2 * side_thickness - 2 * rib_thickness) / 3.0
panel_height = (height - band_height) / 2.0

# Create base box
result = cq.Workplane("XY").box(width, height, depth)

# Cut recessed panels on front face
points = []
for i in range(3):
    x = -width / 2 + side_thickness + panel_width / 2 + i * (panel_width + rib_thickness)
    for j in range(2):
        if j == 0:
            y = band_height / 2 + panel_height / 2
        else:
            y = -band_height / 2 - panel_height / 2
        points.append((x, y))

result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(points)
    .rect(panel_width, panel_height)
    .cutBlind(panel_depth)
)

# Extrude horizontal band on front face
result = (
    result
    .faces(">Z")
    .workplane()
    .rect(width, band_height)
    .extrude(band_depth)
)