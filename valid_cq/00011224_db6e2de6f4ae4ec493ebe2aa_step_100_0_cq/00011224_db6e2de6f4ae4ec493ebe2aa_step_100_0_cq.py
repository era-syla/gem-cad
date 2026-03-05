import cadquery as cq

# --- Parametric Dimensions ---
# Main plate dimensions
plate_width = 80.0
plate_height = 80.0
plate_thickness = 10.0
corner_radius = 5.0

# Bottom cutout dimensions
cutout_width = 40.0
cutout_height = 30.0

# Large center mounting holes
large_hole_diameter = 16.0
large_hole_spacing_x = 40.0
large_hole_y_pos = 15.0  # Offset from center Y upwards

# Small mounting holes (corners)
corner_hole_diameter = 6.0
corner_hole_margin = 6.0 # Distance from edge to hole center

# Inner small holes (near large holes)
inner_hole_diameter = 6.0
inner_hole_offset_x = 10.0 # Relative to large hole center
inner_hole_offset_y = -18.0 # Relative to large hole center (downwards)

# Side holes (drilled into the thickness)
side_hole_diameter = 5.0
side_hole_spacing = 20.0
side_hole_z_offset = 0.0 # Centered in thickness

# --- Construction ---

# 1. Base Plate Shape
# Start with a rectangle and fillet corners
base = (
    cq.Workplane("XY")
    .box(plate_width, plate_height, plate_thickness)
    .edges("|Z")
    .fillet(corner_radius)
)

# 2. Bottom Rectangular Cutout
# Cut a rectangle from the bottom edge
base = base.faces("<Y").workplane().center(0, 0).rect(cutout_width, plate_thickness * 2).cutThruAll()

# We need to re-orient to the main face to drill the holes
# Since we cut from the bottom, the "front" face is +Z relative to the initial box creation,
# but let's just select the largest planar face perpendicular to Z.
face_plane = base.faces(">Z").workplane()

# 3. Corner Holes
# Calculate positions based on width/height and margin
# Top Left, Top Right, Bottom Left (on leg), Bottom Right (on leg)
# Note: Since the bottom middle is cut out, the bottom holes are on the "legs"
# Coordinates relative to center (0,0)
ch_x = (plate_width / 2) - corner_hole_margin
ch_y_top = (plate_height / 2) - corner_hole_margin
ch_y_bot = -(plate_height / 2) + corner_hole_margin

corner_pts = [
    (-ch_x, ch_y_top), (ch_x, ch_y_top),  # Top corners
    (-ch_x, ch_y_bot), (ch_x, ch_y_bot)   # Bottom leg corners
]

base = face_plane.pushPoints(corner_pts).hole(corner_hole_diameter)

# 4. Large Center Holes
# Two large holes side-by-side
large_hole_pts = [
    (-large_hole_spacing_x / 2, large_hole_y_pos),
    (large_hole_spacing_x / 2, large_hole_y_pos)
]

base = base.pushPoints(large_hole_pts).hole(large_hole_diameter)

# 5. Inner Small Holes
# Located relative to the large holes
inner_hole_pts = [
    (-large_hole_spacing_x / 2 + inner_hole_offset_x, large_hole_y_pos + inner_hole_offset_y), # Left side inner
    (large_hole_spacing_x / 2 + inner_hole_offset_x, large_hole_y_pos + inner_hole_offset_y)   # Right side inner (asymmetric pattern in image?)
    # Looking closely at the image, the small holes near the big ones are not perfectly symmetric or mirrored.
    # The left one is below-right of the left big hole.
    # The right one is below-right of the right big hole.
    # Wait, looking again at the image, there are actually TWO small holes near the left big hole region?
    # No, looking at the left side, there is one below the big hole.
    # Looking at the right side, there are two small holes below the big hole.
    # Let's approximate based on standard stepper motor mounts (NEMA 17/23 brackets usually follow patterns).
    # However, to match the visual strictly:
    # Left side: One hole below the big hole.
    # Right side: Two holes below the big hole.
]

# Let's refine the points based on visual inspection of the specific provided image.
# Left side cluster
left_cluster_x = -large_hole_spacing_x / 2
left_cluster_y = large_hole_y_pos
p1 = (left_cluster_x, left_cluster_y - 20) # Directly below left big hole

# Right side cluster
right_cluster_x = large_hole_spacing_x / 2
right_cluster_y = large_hole_y_pos
p2 = (right_cluster_x, right_cluster_y - 20) # Directly below right big hole
p3 = (right_cluster_x + 8, right_cluster_y - 12) # Offset to the right and slightly up from p2

specific_inner_holes = [p1, p2, p3]
base = base.pushPoints(specific_inner_holes).hole(inner_hole_diameter)


# 6. Side Holes (on the left edge thickness)
# Select the face on the -X side
base = base.faces("<X").workplane()

# Create holes. The workplane is now on the side. 
# X axis of workplane runs along global Y, Y axis of workplane runs along global Z usually.
# Let's place two holes on the left leg.
side_hole_pts = [
    (-plate_height/2 + 15, 0), # Bottom one (approximate)
    (-plate_height/2 + 35, 0)  # Top one (approximate)
]
# Note: 'hole' depth is automatic, but here we want to drill into the plate width direction.
# Since we selected the face, hole() goes normal to it (into the material).
base = base.pushPoints(side_hole_pts).hole(side_hole_diameter, depth=15)

result = base