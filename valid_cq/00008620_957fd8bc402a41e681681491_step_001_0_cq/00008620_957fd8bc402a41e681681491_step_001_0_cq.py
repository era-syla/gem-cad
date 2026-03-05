import cadquery as cq

# --- Parametric Definitions ---
# Overall plate dimensions
length = 400.0  # Total length of the plate
width = 100.0   # Total width of the plate
thickness = 3.0 # Thickness of the plate

# Hole parameters
hole_diameter = 4.0
edge_margin = 10.0  # Distance from the edge of the plate to the center of the holes

# Spacing calculations
# We determine the spacing by specifying how many holes we want along each side
# or by specifying a pitch. Let's aim for a visual match with the image.
# The image shows many holes along the long edge (approx 20-25) and fewer on short edge.

# Let's define the number of intervals (spaces between holes)
long_side_intervals = 30
short_side_intervals = 8

# Calculate the start and end positions for the holes
x_start = -length/2 + edge_margin
x_end = length/2 - edge_margin
y_start = -width/2 + edge_margin
y_end = width/2 - edge_margin

# Generate lists of points for the hole locations
# We need a rectangular pattern along the perimeter.

hole_points = []

# Points along the long edges (top and bottom)
# Step size calculation
x_step = (x_end - x_start) / long_side_intervals
for i in range(long_side_intervals + 1):
    x_pos = x_start + (i * x_step)
    hole_points.append((x_pos, y_start)) # Bottom edge
    hole_points.append((x_pos, y_end))   # Top edge

# Points along the short edges (left and right), excluding corners already added
# Step size calculation
y_step = (y_end - y_start) / short_side_intervals
for i in range(1, short_side_intervals): # range(1, ...) skips the first point (corner)
    y_pos = y_start + (i * y_step)
    hole_points.append((x_start, y_pos)) # Left edge
    hole_points.append((x_end, y_pos))   # Right edge


# --- Geometry Construction ---

# 1. Create the base plate
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
)

# 2. Cut the holes using the generated points
result = (
    result
    .faces(">Z")       # Select the top face
    .workplane()       # Create a workplane on the top face
    .pushPoints(hole_points) # Push the calculated locations onto the stack
    .hole(hole_diameter)     # Cut holes through the plate
)