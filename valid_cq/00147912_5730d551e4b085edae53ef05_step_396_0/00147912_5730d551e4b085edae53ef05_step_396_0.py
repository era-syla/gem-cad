import cadquery as cq

# --- Parameters ---
length = 300.0
width = 160.0
thickness = 6.0
fillet_radius = 40.0

# Feature dimensions
large_hole_dia = 15.0
mount_hole_dia = 4.0
corner_hole_dia = 6.0

# Positioning
corner_inset = 12.0
cluster_offset = 40.0  # Center of the rounded corner features
mount_pattern_radius = 14.0

# --- Geometry Generation ---

# 1. Base Plate
# Create rectangle starting at origin (0,0) to simplify coordinate calculation
result = cq.Workplane("XY").rect(length, width, centered=False).extrude(thickness)

# 2. Fillet the bottom-left corner (Origin)
# Select vertical edge at (0,0)
result = result.edges("|Z and <X and <Y").fillet(fillet_radius)

# --- Hole Definitions ---

# Cluster Center (Bottom-Left)
cluster_center = (cluster_offset, cluster_offset)

# Mounting holes pattern around the large hole
# Three holes: Left (-X), Down (-Y), and Diagonal Inward (+X, +Y)
mh1 = (cluster_center[0] - mount_pattern_radius, cluster_center[1])
mh2 = (cluster_center[0], cluster_center[1] - mount_pattern_radius)
# Diagonal offset for 45 degrees
diag_dist = mount_pattern_radius * 0.7071
mh3 = (cluster_center[0] + diag_dist, cluster_center[1] + diag_dist)

mount_hole_pts = [mh1, mh2, mh3]

# Corner holes locations
# Top-Left (near Y-axis) and Top-Right (far diagonal corner)
corner_pts = [
    (corner_inset, width - corner_inset),
    (length - corner_inset, width - corner_inset)
]

# --- Cut Features ---

# Use separate operations to ensure clean updates to the model geometry
# 1. Cut Large Hole
result = result.faces(">Z").workplane().pushPoints([cluster_center]).hole(large_hole_dia)

# 2. Cut Mounting Holes
result = result.faces(">Z").workplane().pushPoints(mount_hole_pts).hole(mount_hole_dia)

# 3. Cut Corner Holes
result = result.faces(">Z").workplane().pushPoints(corner_pts).hole(corner_hole_dia)