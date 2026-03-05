import cadquery as cq
import math

# Parameters
shaft_d = 6.0
shaft_l = 20.0
head_d = 12.0
head_cyl_h = 1.5
head_dome_h = 3.0
hex_w = 4.0
hex_depth = 2.5

# Calculate dome radius
r = head_d / 2.0
h = head_dome_h
dome_radius = (h**2 + r**2) / (2 * h)

# Create the main profile and revolve
profile = (
    cq.Workplane("XZ")
    .moveTo(0, -shaft_l)
    .lineTo(shaft_d / 2, -shaft_l)
    .lineTo(shaft_d / 2, 0)
    .lineTo(head_d / 2, 0)
    .lineTo(head_d / 2, head_cyl_h)
    .radiusArc((0, head_cyl_h + head_dome_h), dome_radius)
    .close()
)

# Revolve around the local Y-axis (which is the global Z-axis for the XZ plane)
result = profile.revolve(360, (0, 0, 0), (0, 1, 0))

# Calculate circumscribed diameter for the hexagon
circum_d = 2 * hex_w / math.sqrt(3)

# Create the hexagonal socket cut
hex_cut = (
    cq.Workplane("XY")
    .workplane(offset=head_cyl_h + head_dome_h)
    .polygon(6, circum_d)
    .extrude(-hex_depth)
)

result = result.cut(hex_cut)

# Add a slight chamfer to the bottom of the screw shaft
result = result.edges("<Z").chamfer(0.5)
