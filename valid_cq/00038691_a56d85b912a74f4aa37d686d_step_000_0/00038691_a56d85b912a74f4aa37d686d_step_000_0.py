import cadquery as cq

# Parametric dimensions
radius = 10.0       # Radius of the hemispheres
spacing = 25.0      # Center-to-center distance between hemispheres
count = 4           # Number of hemispheres

# Define the base hemisphere shape
# 1. Create a full sphere centered at the origin
# 2. Create a box representing the space below the XY plane (Z < 0)
# 3. Cut the sphere with the box to leave only the top half
hemisphere = (
    cq.Workplane("XY")
    .sphere(radius)
    .cut(
        cq.Workplane("XY")
        .rect(radius * 3, radius * 3)  # Large enough to cover the sphere width
        .extrude(-radius * 1.5)        # Extrude downwards to cover the bottom half
    )
)

# Define the locations for the array
points = [(i * spacing, 0, 0) for i in range(count)]

# Create the final result by placing the hemisphere at each point
result = (
    cq.Workplane("XY")
    .pushPoints(points)
    .eachpoint(lambda loc: hemisphere.val().located(loc))
)