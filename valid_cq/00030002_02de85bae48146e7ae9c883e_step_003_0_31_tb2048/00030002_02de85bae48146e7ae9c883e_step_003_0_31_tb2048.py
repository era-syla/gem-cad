import cadquery as cq

# Parameters
major_radius = 50.0  # Radius of the ring itself
minor_radius = 1.5   # Radius of the cross-section (thickness)

# Create the path for the sweep (a circle in the XY plane)
path = cq.Workplane("XY").circle(major_radius)

# Create the profile (a circle in the XZ plane, offset by major_radius) and sweep it along the path
result = (
    cq.Workplane("XZ")
    .center(major_radius, 0)
    .circle(minor_radius)
    .sweep(path)
)