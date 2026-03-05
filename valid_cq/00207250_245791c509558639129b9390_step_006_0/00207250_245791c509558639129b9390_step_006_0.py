import cadquery as cq
import math

# --- Parameters ---
# Plate dimensions
plate_length = 200.0
plate_width = 100.0
plate_thickness = 5.0

# Main cutout dimensions
hole_diameter = 80.0
hole_radius = hole_diameter / 2.0
hole_spacing = 100.0  # Distance between the two main hole centers

# Notch dimensions (small circular cutout on rim)
notch_diameter = 8.0
notch_angle = 45.0  # Angle in degrees for notch orientation

# Mounting hole dimensions
mount_hole_diameter = 4.0
mount_hole_pattern_size = 86.0  # Side length of the square mounting pattern

# --- Geometry Generation ---

# 1. Create the base plate centered at origin
result = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# Define centers for the two stations
# Center of left hole
center_left = (-hole_spacing / 2.0, 0)
# Center of right hole
center_right = (hole_spacing / 2.0, 0)

# 2. Cut the two main large holes
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([center_left, center_right])
    .hole(hole_diameter)
)

# 3. Cut the notches
# Calculate notch positions on the perimeter of the main holes
notch_points = []

# Left hole notch: Bottom-Right quadrant (-45 degrees)
angle_left_rad = math.radians(-notch_angle)
nx_left = center_left[0] + hole_radius * math.cos(angle_left_rad)
ny_left = center_left[1] + hole_radius * math.sin(angle_left_rad)
notch_points.append((nx_left, ny_left))

# Right hole notch: Bottom-Left quadrant (180 + 45 degrees)
angle_right_rad = math.radians(180 + notch_angle)
nx_right = center_right[0] + hole_radius * math.cos(angle_right_rad)
ny_right = center_right[1] + hole_radius * math.sin(angle_right_rad)
notch_points.append((nx_right, ny_right))

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(notch_points)
    .hole(notch_diameter)
)

# 4. Cut the mounting holes
# Generate the 4 corner points for each station
mount_points = []
offset = mount_hole_pattern_size / 2.0

for center in [center_left, center_right]:
    cx, cy = center
    mount_points.append((cx + offset, cy + offset)) # Top Right
    mount_points.append((cx - offset, cy + offset)) # Top Left
    mount_points.append((cx - offset, cy - offset)) # Bottom Left
    mount_points.append((cx + offset, cy - offset)) # Bottom Right

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(mount_points)
    .hole(mount_hole_diameter)
)