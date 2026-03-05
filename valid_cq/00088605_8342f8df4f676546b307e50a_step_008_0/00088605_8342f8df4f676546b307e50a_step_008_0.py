import cadquery as cq
import math

# --- Parameters ---
# Overall dimensions
blade_length = 750.0
handle_length = 250.0
blade_width_base = 32.0
blade_thickness_base = 7.0
curve_height = 90.0  # Vertical curvature displacement at the tip

# Handguard (Tsuba) dimensions
guard_radius_outer = 45.0
guard_radius_inner = 15.0
guard_thickness = 10.0
guard_points = 6

# --- Helper Functions ---
def get_star_profile(r_outer, r_inner, n_points):
    """Generates a list of (x, y) coordinates for a star shape."""
    pts = []
    angle_step = 2 * math.pi / (n_points * 2)
    for i in range(n_points * 2):
        r = r_outer if i % 2 == 0 else r_inner
        a = i * angle_step
        # Coordinates in the local 2D plane
        pts.append((r * math.cos(a), r * math.sin(a)))
    return pts

# --- Modeling ---

# 1. Handle (Tsuka)
# Modeled as a rectangular prism with filleted edges, extending into -X
handle = (
    cq.Workplane("YZ")
    .rect(blade_thickness_base + 12, blade_width_base - 8)
    .extrude(-handle_length)
    .edges("|X").fillet(6)
)

# 2. Handguard (Tsuba)
# Star shape centered at origin
guard_pts = get_star_profile(guard_radius_outer, guard_radius_inner, guard_points)

guard = (
    cq.Workplane("YZ")
    .workplane(offset=-guard_thickness / 2)
    .polyline(guard_pts).close()
    .extrude(guard_thickness)
)

# 3. Blade
# Modeled using a Loft operation through 3 cross-sections to create the taper and curve.
# Coordinate system: X is length, Y is curve direction, Z is thickness.

# Define cross-section geometry (Diamonds)
# Points order for diamond: (Y+, Z0), (Y0, Z+), (Y-, Z0), (Y0, Z-) in global terms
# In "YZ" local plane: local X=Global Y, local Y=Global Z

# Section 1: Base (at Guard)
s1_w = blade_width_base
s1_t = blade_thickness_base
# Vertices for a diamond shape
p1 = [(s1_w/2, 0), (0, s1_t/2), (-s1_w/2, 0), (0, -s1_t/2)]

# Section 2: Mid-blade (Curving up and tapering)
mid_x = blade_length * 0.6
mid_y_shift = curve_height * 0.25
s2_w = blade_width_base * 0.75
s2_t = blade_thickness_base * 0.70
p2 = [(s2_w/2, 0), (0, s2_t/2), (-s2_w/2, 0), (0, -s2_t/2)]

# Section 3: Tip (Curving up more and tapering to a point)
tip_x = blade_length
tip_y_shift = curve_height
s3_w = 0.5  # Very small tip
s3_t = 0.5
p3 = [(s3_w/2, 0), (0, s3_t/2), (-s3_w/2, 0), (0, -s3_t/2)]

# Create the Loft
# Note: .workplane(offset=...) creates a new plane relative to the *previous* one
# .center(x, y) shifts the local origin relative to the *previous* origin
blade = (
    cq.Workplane("YZ")
    
    # Wire 1: Base
    .polyline(p1).close()
    
    # Wire 2: Mid Section
    .workplane(offset=mid_x)
    .center(mid_y_shift, 0)
    .polyline(p2).close()
    
    # Wire 3: Tip Section
    .workplane(offset=tip_x - mid_x)
    .center(tip_y_shift - mid_y_shift, 0)
    .polyline(p3).close()
    
    .loft()
)

# Combine all parts
result = handle.union(guard).union(blade)

# Optional: Rotate for better isometric viewing if exported directly, 
# but result variable usually expects standard alignment.
# keeping alignment along X axis.