import cadquery as cq

def make_rod_bundle(num_rods, rod_length, rod_diameter, spacing):
    """Create a bundle of parallel rods arranged in a row."""
    bundle = None
    for i in range(num_rods):
        x_offset = i * spacing
        rod = (
            cq.Workplane("XY")
            .center(x_offset, 0)
            .circle(rod_diameter / 2)
            .extrude(rod_length)
        )
        if bundle is None:
            bundle = rod
        else:
            bundle = bundle.union(rod)
    return bundle

# Rod parameters
rod_diameter = 2.0
spacing = rod_diameter * 1.2
num_rods = 10

# Long bundle (top-left in image) - longest rods
long_length = 120.0
long_bundle = make_rod_bundle(num_rods, long_length, rod_diameter, spacing)

# Medium bundle (middle) - about half length
medium_length = 60.0
medium_bundle = make_rod_bundle(num_rods, medium_length, rod_diameter, spacing)

# Short bundle (bottom-right) - about quarter length
short_length = 30.0
short_bundle = make_rod_bundle(num_rods, short_length, rod_diameter, spacing)

# Position bundles to match the image layout
# Long bundle at top-left
long_positioned = long_bundle.translate((0, 0, 0))

# Medium bundle offset down and to the right
medium_offset_x = 30
medium_offset_y = -30
medium_positioned = medium_bundle.translate((medium_offset_x, medium_offset_y, 0))

# Short bundle further down and to the right
short_offset_x = 55
short_offset_y = -55
short_positioned = short_bundle.translate((short_offset_x, short_offset_y, 0))

# Combine all bundles
result = long_positioned.union(medium_positioned).union(short_positioned)