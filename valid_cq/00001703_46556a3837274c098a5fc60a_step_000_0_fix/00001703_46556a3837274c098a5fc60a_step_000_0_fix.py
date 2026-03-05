import cadquery as cq

# Parameters
num_rails = 3
spacing = 5.0
rail_width = 2.0
rail_height = 1.0
straight_length = 80.0
arc_radius = 20.0

# Build the sweep path in the XY plane: straight segment then 90° arc
path = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(straight_length, 0)
    .radiusArc((straight_length, arc_radius), arc_radius)
    .wire()
)

# Create a single rail by sweeping a rectangle along the path
profile = cq.Workplane("XY").rect(rail_width, rail_height)
single_rail = profile.sweep(path)

# Array the rails and union them together
result = None
for i in range(num_rails):
    offset = (i - (num_rails - 1) / 2.0) * spacing
    rail = single_rail.translate((0, offset, 0))
    result = rail if result is None else result.union(rail)