import cadquery as cq

# Parametric dimensions
cube_size = 10.0
spacing = 50.0

# Define the coordinates for the cubes.
# In a standard isometric view:
# - (d, d) appears to the Right
# - (-d, -d) appears to the Left
# - (-d, d) appears at the Top
# - (d, -d) appears at the Bottom
points = [
    (0, 0),                       # Center
    (spacing, spacing),           # Right
    (-spacing, -spacing),         # Left
    (-spacing, spacing),          # Top
    (spacing, -spacing)           # Bottom
]

# Create the 3D model
result = (
    cq.Workplane("XY")
    .pushPoints(points)
    .box(cube_size, cube_size, cube_size)
)