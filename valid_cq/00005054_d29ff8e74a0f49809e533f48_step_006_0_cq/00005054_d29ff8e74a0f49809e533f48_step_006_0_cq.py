import cadquery as cq

# Parameters for the rings
inner_diameter = 10.0
wall_thickness = 0.5
height = 5.0
spacing_x = 20.0  # Distance between centers in X
spacing_y = 15.0  # Distance between centers in Y

# Derived parameters
outer_diameter = inner_diameter + (2 * wall_thickness)
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0

# Function to create a single ring
def create_ring():
    return (
        cq.Workplane("XY")
        .circle(outer_radius)
        .circle(inner_radius)
        .extrude(height)
    )

# Create the first ring at the origin
ring1 = create_ring()

# Create the second ring offset by the spacing values
ring2 = create_ring().translate((spacing_x, spacing_y, 0))

# Combine the two rings into a single object
result = ring1.union(ring2)