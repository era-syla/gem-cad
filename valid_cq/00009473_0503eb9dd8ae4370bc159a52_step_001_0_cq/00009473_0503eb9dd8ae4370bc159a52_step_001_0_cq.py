import cadquery as cq

# Parameters for the rods
rod_diameter = 5.0
tall_rod_height = 200.0
short_rod_height = 150.0
spacing = 15.0  # Distance between centers

# Create the tall rod
# We'll position it slightly to the left (-spacing/2)
tall_rod = (
    cq.Workplane("XY")
    .center(-spacing / 2.0, 0)
    .circle(rod_diameter / 2.0)
    .extrude(tall_rod_height)
)

# Create the short rod
# We'll position it slightly to the right (spacing/2)
short_rod = (
    cq.Workplane("XY")
    .center(spacing / 2.0, 0)
    .circle(rod_diameter / 2.0)
    .extrude(short_rod_height)
)

# Combine the two rods into a single result
result = tall_rod.union(short_rod)