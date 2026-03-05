import cadquery as cq

# Parametric dimensions
major_radius = 40.0
minor_radius = 3.0

# Create the ring geometry by revolving a circular cross-section
result = (
    cq.Workplane("XZ")
    .center(major_radius, 0)
    .circle(minor_radius)
    .revolve(360, (0, 0, 0), (0, 0, 1))
)