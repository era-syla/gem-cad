import cadquery as cq

# Dimensions
plate_length = 60.0
plate_width = 25.0
plate_thickness = 3.0
fillet_radius = 4.0
hole_diameter = 4.0

# Define shapes for the text cutouts
# Characters: 7, L, N
# We define them relative to a local origin (bottom-left of the character box)
# and then shift them to the correct position on the plate.
# Character Box Height: 16mm
# Character Box Widths: ~10-11mm
# Stroke Thickness: ~3mm

def get_7_pts(offset_x, offset_y):
    # '7' shape points
    # Calculated to maintain approx 3mm thickness for diagonal and top bar
    # Local coords (0,0) to (10,16)
    pts = [
        (0, 16),      # Top-left
        (10, 16),     # Top-right
        (4.0, 0),     # Bottom tip of diagonal
        (1.0, 0),     # Inner bottom tip
        (5.875, 13),  # Inner corner (calculated for parallel lines)
        (0, 13)       # Bottom of top bar
    ]
    return [(x + offset_x, y + offset_y) for x, y in pts]

def get_L_pts(offset_x, offset_y):
    # 'L' shape points
    pts = [
        (0, 16), (3, 16),  # Vertical top
        (3, 3),            # Inner corner
        (10, 3), (10, 0),  # Horizontal end
        (0, 0)             # Bottom-left corner
    ]
    return [(x + offset_x, y + offset_y) for x, y in pts]

def get_N_pts(offset_x, offset_y):
    # 'N' shape points
    # Stylized with vertical bars and diagonal
    pts = [
        (0, 0), (0, 16),       # Left vertical outer
        (3.5, 16),             # Top diagonal start (slightly wide)
        (8, 6),                # Inner diagonal intersection
        (8, 16), (11, 16),     # Right vertical top
        (11, 0),               # Right vertical bottom
        (7.5, 0),              # Bottom diagonal start
        (3, 10),               # Inner diagonal intersection
        (3, 0)                 # Left vertical bottom
    ]
    return [(x + offset_x, y + offset_y) for x, y in pts]

# Calculate positions to center text
# Total width approx 10+3+10+3+11 = 37mm
# Center of plate is (0,0)
# Start X around -13 to shift slightly right due to keyhole on left
y_base = -8.0 # Centered vertically (16mm height, -8 to 8)
pts_7 = get_7_pts(-13, y_base)
pts_L = get_L_pts(0, y_base)
pts_N = get_N_pts(13, y_base)

# Create the Base Plate
result = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_thickness)
    .edges("|Z")
    .fillet(fillet_radius)
)

# Create Text Cutouts
# We sketch on the top face and cut through
result = (
    result.faces(">Z")
    .workplane()
    .polyline(pts_7).close()
    .polyline(pts_L).close()
    .polyline(pts_N).close()
    .cutBlind(-plate_thickness)
)

# Create Keyhole
# Positioned in the bottom-left corner, concentric with the fillet
# Corner is at (-30, -12.5), Fillet R=4 -> Center approx (-26, -8.5)
keyhole_center_x = -plate_length/2 + fillet_radius
keyhole_center_y = -plate_width/2 + fillet_radius

result = (
    result.faces(">Z")
    .workplane()
    .moveTo(keyhole_center_x, keyhole_center_y)
    .hole(hole_diameter)
)