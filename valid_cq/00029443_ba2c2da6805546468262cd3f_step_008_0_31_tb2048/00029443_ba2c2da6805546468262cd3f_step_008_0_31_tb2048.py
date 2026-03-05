import cadquery as cq

# Parameters for the L-bracket
length = 360.0
width = 15.0
height = 15.0
thickness = 2.0
hole_dia = 4.0
hole_spacing = 12.0
num_holes = 29

# Create the L-profile on the YZ plane
profile = cq.Workplane("YZ").polyline([
    (0, 0),
    (width, 0),
    (width, thickness),
    (thickness, thickness),
    (thickness, height),
    (0, height)
]).close()

# Extrude symmetrically along the X-axis
bracket = profile.extrude(length / 2, both=True)

# Add fillets to the outer corners of the flanges at the ends
bracket = bracket.edges("|Z").edges(">Y").fillet(2.0)
bracket = bracket.edges("|Y").edges(">Z").fillet(2.0)

# Add small fillets to the longitudinal edges for a realistic sheet metal look
bracket = bracket.edges("|X").fillet(0.5)

# Calculate X positions for the holes (centered along the length)
hole_x_positions = [(i - (num_holes - 1) / 2) * hole_spacing for i in range(num_holes)]

# Hole coordinates on their respective flanges
base_hole_y = (width + thickness) / 2.0
wall_hole_z = (height + thickness) / 2.0

# Cut holes in the base flange (bottom)
base_wp = cq.Workplane("XY").workplane(offset=thickness * 2)
base_pts = [(x, base_hole_y) for x in hole_x_positions]
bracket = bracket.cut(base_wp.pushPoints(base_pts).circle(hole_dia / 2).extrude(-thickness * 4))

# Cut holes in the vertical flange (wall)
wall_wp = cq.Workplane("XZ").workplane(offset=thickness * 2)
wall_pts = [(x, wall_hole_z) for x in hole_x_positions]
bracket = bracket.cut(wall_wp.pushPoints(wall_pts).circle(hole_dia / 2).extrude(-thickness * 4))

# Final geometry
result = bracket