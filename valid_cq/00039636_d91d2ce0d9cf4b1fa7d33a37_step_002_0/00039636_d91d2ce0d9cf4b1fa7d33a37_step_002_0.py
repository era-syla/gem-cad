import cadquery as cq

# Geometric Parameters
bend_radius = 50.0        # Distance from center of revolution to center of pipe
pipe_outer_radius = 25.0  # Radius of the outer pipe surface
wall_thickness = 4.0      # Thickness of the material
bend_angle = 180.0        # Angle of the elbow (180 degrees)

# Calculated Parameters
pipe_inner_radius = pipe_outer_radius - wall_thickness

# Create the Elbow Model
# 1. Create a Workplane on the XY plane.
# 2. Move to the bend radius to define the offset for revolution.
# 3. Draw the outer and inner circles to define the hollow pipe profile.
# 4. Revolve the profile around the Y-axis to create the bent geometry.
result = (
    cq.Workplane("XY")
    .moveTo(bend_radius, 0)
    .circle(pipe_outer_radius)
    .circle(pipe_inner_radius)
    .revolve(bend_angle, (0, 0, 0), (0, 1, 0))
)