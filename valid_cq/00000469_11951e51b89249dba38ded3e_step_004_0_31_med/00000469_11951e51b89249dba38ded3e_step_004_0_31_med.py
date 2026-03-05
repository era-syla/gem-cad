import cadquery as cq

# Parameters
major_radius = 50.0  # Radius of the main ring path
minor_radius = 3.5   # Radius of the circular cross-section

# Create the torus (O-ring) geometry
result = (
    cq.Workplane("XZ")
    .moveTo(major_radius, 0)
    .circle(minor_radius)
    .revolve(360, (0, 0, 0), (0, 1, 0))
)