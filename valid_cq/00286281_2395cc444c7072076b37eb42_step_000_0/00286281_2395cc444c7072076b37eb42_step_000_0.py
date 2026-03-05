import cadquery as cq

# Parametric dimensions for the grooved pipe
length = 200.0          # Total length of the pipe
outer_diameter = 20.0   # Outer diameter
wall_thickness = 1.5    # Wall thickness
groove_width = 3.0      # Width of the groove near the ends
groove_depth = 0.6      # Depth of the groove cut into the outer surface
groove_offset = 6.0     # Distance from the end of the pipe to the start of the groove

# Derived dimensions
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

# Define the profile points for the cross-section of the pipe wall
# We define the profile in the XZ plane to revolve around the Z axis
# Coordinates are (radius, height)
points = [
    (inner_radius, 0),                                      # Bottom inner corner
    (outer_radius, 0),                                      # Bottom outer corner
    (outer_radius, groove_offset),                          # Start of bottom groove
    (outer_radius - groove_depth, groove_offset),           # Bottom of groove (start)
    (outer_radius - groove_depth, groove_offset + groove_width), # Bottom of groove (end)
    (outer_radius, groove_offset + groove_width),           # End of bottom groove
    (outer_radius, length - groove_offset - groove_width),  # Start of top groove
    (outer_radius - groove_depth, length - groove_offset - groove_width), # Bottom of top groove (start)
    (outer_radius - groove_depth, length - groove_offset),  # Bottom of top groove (end)
    (outer_radius, length - groove_offset),                 # End of top groove
    (outer_radius, length),                                 # Top outer corner
    (inner_radius, length)                                  # Top inner corner
]

# Create the 3D model by revolving the profile
result = (
    cq.Workplane("XZ")
    .polyline(points)
    .close()
    .revolve()
)