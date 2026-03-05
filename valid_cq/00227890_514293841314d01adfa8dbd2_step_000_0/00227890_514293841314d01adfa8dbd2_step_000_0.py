import cadquery as cq

# Parametric dimensions
outer_diameter = 20.0
wall_thickness = 2.0
inner_diameter = outer_diameter - (2 * wall_thickness)

long_tube_length = 250.0
short_tube_length = 50.0

# Positioning parameters
separation_distance = 40.0  # Lateral distance between tube axes
short_tube_offset = 180.0   # Offset of the short tube along the main axis

# Create the long tube
long_tube = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(long_tube_length)
)

# Create the short tube (coupler)
short_tube = (
    cq.Workplane("XY")
    .workplane(offset=short_tube_offset)
    .center(separation_distance, 0)
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(short_tube_length)
)

# Combine both objects into the final result
result = long_tube.union(short_tube)