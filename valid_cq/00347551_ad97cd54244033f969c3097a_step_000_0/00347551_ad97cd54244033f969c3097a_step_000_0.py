import cadquery as cq

# Parametric dimensions for the shaft
total_length = 80.0
shaft_diameter = 8.0
groove_diameter = 6.5
groove_width = 1.0
end_distance = 4.0    # Distance from the end face to the start of the groove
chamfer_size = 0.5

# Calculate radii
shaft_radius = shaft_diameter / 2.0
groove_radius = groove_diameter / 2.0

# Define the 2D profile points for revolution
# Coordinate system: X is the axis of the shaft, Y is radial distance
points = [
    (0, 0),                                           # Center at start
    (total_length, 0),                                # Center at end
    (total_length, shaft_radius),                     # Outer edge at end
    (total_length - end_distance, shaft_radius),      # Start of far groove
    (total_length - end_distance, groove_radius),     # Down into far groove
    (total_length - end_distance - groove_width, groove_radius), # Bottom of far groove
    (total_length - end_distance - groove_width, shaft_radius),  # Up from far groove
    (end_distance + groove_width, shaft_radius),      # Start of near groove
    (end_distance + groove_width, groove_radius),     # Down into near groove
    (end_distance, groove_radius),                    # Bottom of near groove
    (end_distance, shaft_radius),                     # Up from near groove
    (0, shaft_radius),                                # Outer edge at start
    (0, 0)                                            # Close loop to center
]

# Create the solid by revolving the profile around the X-axis
result = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .revolve(360, (0, 0, 0), (1, 0, 0))
)

# Apply chamfers to the edges of the end faces
# Selects faces with normals pointing in -X and +X directions
result = result.faces("<X or >X").edges().chamfer(chamfer_size)