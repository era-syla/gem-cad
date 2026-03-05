import cadquery as cq

# Define the coordinates for the outline of Texas
# Note: These are simplified coordinates to approximate the shape.
# A highly detailed map would require many more points.
points = [
    (0.0, 0.0), # Start near El Paso
    (5.0, 0.0), # Straight bottom edge (Mexico border simplified)
    (5.0, 5.0), # Right side near the Gulf
    (10.0, 10.0), # Panhandle right side
    (10.0, 15.0), # Panhandle top right
    (5.0, 15.0), # Panhandle top left
    (5.0, 10.0), # Panhandle left side
    (0.0, 5.0), # West side
]

# Create a workplane and build the 2D profile
texas_profile = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
)

# Extrude the profile to create the 3D model
thickness = 1.0
result = texas_profile.extrude(thickness)