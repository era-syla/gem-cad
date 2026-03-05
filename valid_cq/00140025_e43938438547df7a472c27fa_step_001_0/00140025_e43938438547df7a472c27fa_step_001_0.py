import cadquery as cq

# Model parameters estimated from the image geometry
tube_radius = 5.0       # Radius of the tube cross-section (minor radius)
major_radius = 10.0     # Radius from the center of the ring to the center of the tube
center_spacing = 20.0   # Distance between the centers of the two rings

# Function to create a torus
def create_torus(major_r, minor_r):
    return (
        cq.Workplane("XZ")
        .center(major_r, 0)
        .circle(minor_r)
        .revolve(360, (0, 0, 0), (0, 0, 1))
    )

# Create the two torus objects positioned symmetrically
# Left ring centered at -spacing/2
ring_left = create_torus(major_radius, tube_radius).translate((-center_spacing / 2, 0, 0))

# Right ring centered at +spacing/2
ring_right = create_torus(major_radius, tube_radius).translate((center_spacing / 2, 0, 0))

# Combine the two rings into the final figure-8 shape
result = ring_left.union(ring_right)