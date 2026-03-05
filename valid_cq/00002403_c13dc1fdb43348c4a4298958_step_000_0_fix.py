import cadquery as cq

# Parameters
shaft_radius = 2.5
shaft_length = 120
base_radius = 5
base_height = 15
notch_width = 2
notch_depth = 1.5
notch_height = 4

# Build the main shaft (thin cylinder)
shaft = (
    cq.Workplane("XY")
    .cylinder(shaft_length, shaft_radius)
    .translate((0, 0, shaft_length / 2 + base_height))
)

# Build the base cylinder (wider, at the bottom)
base = (
    cq.Workplane("XY")
    .cylinder(base_height, base_radius)
    .translate((0, 0, base_height / 2))
)

# Combine shaft and base
combined = base.union(shaft)

# Add a small notch/slot on the side of the base cylinder
notch = (
    cq.Workplane("XY")
    .box(notch_depth * 2 + base_radius * 2, notch_width, notch_height)
    .translate((base_radius, 0, base_height / 2))
)

# Cut the notch from the base area
result = combined.cut(notch)

# Clean up with small fillet on top of shaft
result = (
    result
    .faces(">Z")
    .edges()
    .chamfer(0.3)
)