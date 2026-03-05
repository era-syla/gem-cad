import cadquery as cq

# Parameters for dimensions
num_rows = 2       # Number of rows of cylinders
num_cols = 5       # Number of columns of cylinders
cylinder_radius = 2.0
cylinder_height = 100.0
spacing_x = 4.5    # Center-to-center distance in X
spacing_y = 4.5    # Center-to-center distance in Y

# Base position adjustment to center the array
start_x = -((num_cols - 1) * spacing_x) / 2
start_y = -((num_rows - 1) * spacing_y) / 2

# Create a list of points for the cylinder centers
points = []
for r in range(num_rows):
    for c in range(num_cols):
        x = start_x + c * spacing_x
        y = start_y + r * spacing_y
        points.append((x, y))

# Create the array of cylinders
# We push the points to a sketch plane, draw circles, and extrude them
result = (
    cq.Workplane("XY")
    .pushPoints(points)
    .circle(cylinder_radius)
    .extrude(cylinder_height)
)