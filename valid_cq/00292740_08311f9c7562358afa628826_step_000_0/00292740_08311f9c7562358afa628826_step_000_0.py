import cadquery as cq

# --- Parameters ---
# Profile dimensions (L-angle 40x40x3 mm)
profile_w = 40.0
profile_h = 40.0
profile_t = 3.0

# Structure dimensions
diag_beam_length = 1600.0
horz_beam_length = 1200.0
diag_angle = 60.0          # Angle of diagonal beams in degrees
diag_spacing = 500.0       # Perpendicular spacing between diagonal beams
horz_spacing = 700.0       # Y-axis spacing between horizontal beams

# --- Helper Function ---
def make_l_profile(length, w, h, t):
    """
    Creates an L-angle beam along the X-axis.
    The outer corner of the L is at (0,0,0).
    Vertical leg points +Z, Horizontal leg points +Y.
    """
    # Define points for L-profile on YZ plane
    pts = [
        (0, 0),
        (w, 0),
        (w, t),
        (t, t),
        (t, h),
        (0, h)
    ]
    
    # Create sketch and extrude
    return (cq.Workplane("YZ")
            .polyline(pts)
            .close()
            .extrude(length))

# --- Geometry Construction ---

# 1. Base Diagonal Beams
# Create the generic beam geometry centered lengthwise
base_diag = make_l_profile(diag_beam_length, profile_w, profile_h, profile_t)
base_diag = base_diag.translate((-diag_beam_length / 2, 0, 0))

# Position the two diagonal beams
# We offset them in Y first, then rotate around Z to achieve parallel spacing
offset_dist = diag_spacing / 2.0

diag1 = base_diag.translate((0, -offset_dist, 0)).rotate((0,0,0), (0,0,1), diag_angle)
diag2 = base_diag.translate((0, offset_dist, 0)).rotate((0,0,0), (0,0,1), diag_angle)


# 2. Top Horizontal Beams
# Create the generic beam geometry centered lengthwise
base_horz = make_l_profile(horz_beam_length, profile_w, profile_h, profile_t)
base_horz = base_horz.translate((-horz_beam_length / 2, 0, 0))

# Determine Z height for the top layer
# They sit on top of the vertical leg of the diagonal beams
z_height = profile_h

# Position the two horizontal beams
horz1 = base_horz.translate((0, horz_spacing / 2, z_height))
horz2 = base_horz.translate((0, -horz_spacing / 2, z_height))

# --- Final Assembly ---
result = diag1.union(diag2).union(horz1).union(horz2)