import cadquery as cq

# --- Parameter Definitions ---

# Plate Dimensions
plate_length = 240.0
plate_height = 60.0
plate_thickness = 5.0

# Feature Layout Parameters
# The plate has two groups of features, left and right.
# Each group consists of a 6-hole cluster and a mounting pattern.
group_center_offset = 65.0  # Distance from plate center to group center
feature_spacing = 50.0      # Distance between cluster and mount within a group

# Hole Dimensions
dia_cluster_hole = 10.0
dia_mount_center = 12.0
dia_mount_screw = 4.0

# Pattern Details
# Cluster: 2 rows of 3 holes, staggered
cluster_pitch_x = 15.0
cluster_pitch_y = 14.0
# Mount: Central hole surrounded by 4 screw holes
mount_screw_square_side = 24.0

# --- Helper Functions ---

def get_cluster_locations(center_x, center_y):
    """
    Generates the (x, y) coordinates for a 6-hole staggered cluster.
    Top row: 3 holes centered on center_x.
    Bottom row: 3 holes, staggered left relative to top row.
    """
    pts = []
    # Top Row (y = +half pitch)
    y_top = center_y + cluster_pitch_y / 2.0
    for i in range(3):
        # i=0 -> -pitch, i=1 -> 0, i=2 -> +pitch
        x = center_x + (i - 1) * cluster_pitch_x
        pts.append((x, y_top))
        
    # Bottom Row (y = -half pitch)
    y_bot = center_y - cluster_pitch_y / 2.0
    stagger_offset = cluster_pitch_x / 2.0
    for i in range(3):
        x = center_x + (i - 1) * cluster_pitch_x - stagger_offset
        pts.append((x, y_bot))
        
    return pts

def get_mount_screw_locations(center_x, center_y):
    """
    Generates the (x, y) coordinates for the 4 mounting screws.
    """
    offset = mount_screw_square_side / 2.0
    pts = [
        (center_x - offset, center_y - offset),
        (center_x + offset, center_y - offset),
        (center_x + offset, center_y + offset),
        (center_x - offset, center_y + offset),
    ]
    return pts

# --- Main Geometry Construction ---

# 1. Create the base plate
result = cq.Workplane("XY").box(plate_length, plate_height, plate_thickness)

# 2. Calculate Feature Positions
# Group 1 (Left side)
g1_x = -group_center_offset
c1_x = g1_x - (feature_spacing / 2.0) # Cluster is to the left in the group
m1_x = g1_x + (feature_spacing / 2.0) # Mount is to the right in the group

# Group 2 (Right side)
g2_x = group_center_offset
c2_x = g2_x - (feature_spacing / 2.0) # Cluster is to the left in the group
m2_x = g2_x + (feature_spacing / 2.0) # Mount is to the right in the group

# 3. Gather all hole coordinates
all_cluster_pts = []
all_cluster_pts.extend(get_cluster_locations(c1_x, 0))
all_cluster_pts.extend(get_cluster_locations(c2_x, 0))

all_mount_center_pts = [(m1_x, 0), (m2_x, 0)]

all_mount_screw_pts = []
all_mount_screw_pts.extend(get_mount_screw_locations(m1_x, 0))
all_mount_screw_pts.extend(get_mount_screw_locations(m2_x, 0))

# 4. Cut the holes
result = (result
          .faces(">Z").workplane()
          # Cut Cluster Holes
          .pushPoints(all_cluster_pts)
          .hole(dia_cluster_hole)
          # Cut Mount Center Holes
          .pushPoints(all_mount_center_pts)
          .hole(dia_mount_center)
          # Cut Mount Screw Holes
          .pushPoints(all_mount_screw_pts)
          .hole(dia_mount_screw)
         )