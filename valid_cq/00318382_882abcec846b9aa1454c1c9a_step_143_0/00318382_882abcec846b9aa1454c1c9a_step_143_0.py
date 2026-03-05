import cadquery as cq

# --- Parametric Dimensions ---
# Plate dimensions
plate_length = 160.0
plate_width = 60.0
plate_thickness = 6.0

# Hole specifications
center_hole_diameter = 12.0
small_hole_diameter = 5.2  # M5 clearance

# Feature Locations (relative to plate center)
# The 5-hole cluster location
cluster_center_x = -25.0
cluster_radius = 16.0  # Distance from cluster center to satellite holes

# The paired holes locations
mid_pair_x = 25.0
end_pair_x = 65.0
pair_spacing_y = 40.0  # Vertical distance between holes in a pair

# --- 3D Modeling ---

# 1. Create the base rectangular plate
result = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# 2. Create the large central hole in the cluster
result = result.faces(">Z").workplane().moveTo(cluster_center_x, 0).hole(center_hole_diameter)

# 3. Create the pattern of small holes

# Define points for the cluster satellites (Cross/Diamond pattern)
cluster_points = [
    (cluster_center_x, cluster_radius),            # Top
    (cluster_center_x, -cluster_radius),           # Bottom
    (cluster_center_x + cluster_radius, 0),        # Right
    (cluster_center_x - cluster_radius, 0)         # Left
]

# Define points for the middle pair of holes
mid_pair_points = [
    (mid_pair_x, pair_spacing_y / 2.0),
    (mid_pair_x, -pair_spacing_y / 2.0)
]

# Define points for the end pair of holes
end_pair_points = [
    (end_pair_x, pair_spacing_y / 2.0),
    (end_pair_x, -pair_spacing_y / 2.0)
]

# Combine all small hole locations
all_small_points = cluster_points + mid_pair_points + end_pair_points

# Cut the small holes
result = result.faces(">Z").workplane().pushPoints(all_small_points).hole(small_hole_diameter)