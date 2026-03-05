import cadquery as cq

# --- Parametric Dimensions ---
plate_width = 150.0   # Total width (X-axis)
plate_depth = 120.0   # Total depth (Y-axis)
plate_thickness = 3.0 # Thickness of the plate (Z-axis)
corner_radius = 5.0   # Radius for the rounded corners

# Hole parameters
hole_diameter = 3.5          # Standard hole size
countersink_diameter = 6.0   # Not explicitly visible as countersunk, but good practice for mounting plates
hole_edge_margin = 6.0       # Distance from edge to hole center

# --- Geometry Construction ---

# 1. Base Plate
# Create the base rectangle and extrude it
base = (
    cq.Workplane("XY")
    .box(plate_width, plate_depth, plate_thickness)
    .edges("|Z")  # Select vertical edges
    .fillet(corner_radius)
)

# 2. Define Hole Locations
# Calculate positions relative to the center (0,0)

x_max = plate_width / 2 - hole_edge_margin
y_max = plate_depth / 2 - hole_edge_margin

# Corner holes (4 corners)
corner_locs = [
    (x_max, y_max),
    (-x_max, y_max),
    (x_max, -y_max),
    (-x_max, -y_max),
]

# Side holes (top edge in the image perspective)
# Assuming 2 evenly spaced holes between the top corners
top_edge_y = y_max
side_hole_spacing = plate_width / 3.0 # Simple approximation
side_locs = [
    (side_hole_spacing/2, top_edge_y),
    (-side_hole_spacing/2, top_edge_y),
]

# Cluster of holes (bottom right area in the image perspective)
# This looks like a specific mounting pattern.
# Let's approximate a linear pattern and an offset hole.
cluster_start_x = 10.0
cluster_y = -y_max + 15.0 # Moved slightly inward from bottom edge
cluster_hole_dist = 12.0
cluster_locs = []

# Diagonal/Angled line of holes
for i in range(5):
    # Creating a line of holes angling towards the center right
    cluster_locs.append((cluster_start_x + (i * cluster_hole_dist), cluster_y + (i * cluster_hole_dist * 0.5)))

# Add a couple specific offset holes to match the visual density
cluster_locs.append((cluster_start_x + 10, cluster_y - 10)) # Near bottom edge
cluster_locs.append((cluster_start_x + 35, cluster_y - 5))  # Near bottom edge

# Combine all hole locations into a single list for the main perimeter/side holes
# Note: The specific cluster logic is hard to replicate exactly without dimensions,
# so I will create a simplified representation based on the visual groups.

# Let's redefine based on visual groups more precisely:
# Group A: Top edge (4 holes including corners)
group_a_y = plate_depth/2 - hole_edge_margin
group_a_xs = [-plate_width/2 + hole_edge_margin, 
              -plate_width/6, 
              plate_width/6, 
              plate_width/2 - hole_edge_margin]
group_a = [(x, group_a_y) for x in group_a_xs]

# Group B: Bottom Corners
group_b = [
    (-plate_width/2 + hole_edge_margin, -plate_depth/2 + hole_edge_margin),
    (plate_width/2 - hole_edge_margin, -plate_depth/2 + hole_edge_margin)
]

# Group C: The complex cluster in the bottom-right quadrant
# It looks like a line of 5 holes and 2 holes below it near the edge.
group_c_start_x = 0
group_c_y_base = -plate_depth/2 + 25
group_c_spacing = 15
group_c = []
# The line of 5 holes
for i in range(5):
    group_c.append((group_c_start_x + (i * group_c_spacing), group_c_y_base + (i * 2)))

# The 2 holes below the line
group_c.append((group_c_start_x + group_c_spacing, -plate_depth/2 + hole_edge_margin))
group_c.append((group_c_start_x + group_c_spacing*3, -plate_depth/2 + hole_edge_margin))

all_holes = group_a + group_b + group_c

# 3. Apply Holes
result = (
    base
    .faces(">Z")
    .workplane()
    .pushPoints(all_holes)
    .hole(hole_diameter)
)