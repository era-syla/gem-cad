import cadquery as cq

# Design parameters
radius = 50.0
height = 20.0
center_radius = 16.0
groove_width = 0.4
slit_angle = 210  # Angle to orient the slit visually similar to the image

# Calculate arc radius for the spherical cap
arc_radius = (radius**2 + height**2) / (2 * height)

# Create the solid base dome
dome = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .hLine(radius)
    .radiusArc((0, height), arc_radius)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)

# Create circular groove cutting tool
circle_cut = (
    cq.Workplane("XY")
    .circle(center_radius + groove_width / 2.0)
    .circle(center_radius - groove_width / 2.0)
    .extrude(height + 5.0)
)

# Create radial slit cutting tool
slit_length = radius - center_radius + 5.0
slit_center_x = center_radius + slit_length / 2.0 - 1.0

slit_cut = (
    cq.Workplane("XY")
    .center(slit_center_x, 0)
    .rect(slit_length, groove_width)
    .extrude(height + 5.0)
    .rotate((0, 0, 0), (0, 0, 1), slit_angle)
)

# Apply the cuts to generate the final geometry
result = dome.cut(circle_cut).cut(slit_cut)