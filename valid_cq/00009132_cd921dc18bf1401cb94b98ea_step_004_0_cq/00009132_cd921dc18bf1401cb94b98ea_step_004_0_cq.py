import cadquery as cq

# Parameters
length = 150.0       # Total length of the plate
width = 100.0        # Total width of the plate
thickness = 5.0      # Thickness of the plate
corner_radius = 10.0 # Radius of the rounded corners

# Hole parameters
hole_diameter = 4.0      # Diameter of the through hole
cbore_diameter = 8.0     # Diameter of the counterbore
cbore_depth = 2.0        # Depth of the counterbore
margin = 6.0             # Distance from the edge to the center of the holes

# Calculate hole positions
# We need holes along the perimeter. 
# Based on the image, there are:
# - 4 corner holes
# - 2 intermediate holes on the short sides (total 4 on short sides) -> Actually looking closer, it's just corners on short side? No, looks like 1 in middle of short side.
# - 3 intermediate holes on the long sides (total 5 on long sides).
# Let's count again carefully from the image.
# Long side: Corner, + 3 holes, + Corner = 5 holes per long edge.
# Short side: Corner, + 1 hole, + Corner = 3 holes per short edge.
# Total holes = 2*(5) + 2*(1) = 12 holes?
# Let's look at the spacing.
# The holes seem evenly distributed along the edges.

# Define the main plate
plate = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .edges("|Z")
    .fillet(corner_radius)
)

# Define hole positions
# We will generate a list of (x, y) coordinates for the holes.
# Long side distribution (along X axis):
# x_positions = [-x_max, -x_mid, 0, x_mid, x_max]
# Short side distribution (along Y axis):
# y_positions = [-y_max, 0, y_max]

# Effective dimensions for hole centers
x_center_dist = (length / 2) - margin
y_center_dist = (width / 2) - margin

# Create a list of points. 
# We'll place holes along the top and bottom edges (long sides)
long_side_x_coords = [
    -x_center_dist, 
    -x_center_dist/2, 
    0, 
    x_center_dist/2, 
    x_center_dist
]

holes = []

# Top and Bottom rows (5 holes each)
for x in long_side_x_coords:
    holes.append((x, y_center_dist))   # Top edge
    holes.append((x, -y_center_dist))  # Bottom edge

# Left and Right middle holes (1 hole each)
# The corners are already covered by the top/bottom loops.
# We just need the middle hole on the short edges.
holes.append((-x_center_dist, 0)) # Left edge middle
holes.append((x_center_dist, 0))  # Right edge middle

# Create the holes
result = (
    plate
    .faces(">Z")
    .workplane()
    .pushPoints(holes)
    .cboreHole(hole_diameter, cbore_diameter, cbore_depth)
)