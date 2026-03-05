import cadquery as cq

# Parametric dimensions
outer_diameter = 20.0
wall_thickness = 1.5
long_pipe_length = 120.0
short_pipe_length = 60.0
pipe_spacing = 40.0  # Distance between centers

# Calculate radii
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

# Create the longer tube
# We define concentric circles and extrude to create a hollow cylinder
long_tube = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(long_pipe_length)
)

# Create the shorter tube
# Create geometry and translate it to position it parallel to the first
short_tube = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(short_pipe_length)
    .translate((0, -pipe_spacing, 0))
)

# Combine both tubes into the final result
result = long_tube.union(short_tube)