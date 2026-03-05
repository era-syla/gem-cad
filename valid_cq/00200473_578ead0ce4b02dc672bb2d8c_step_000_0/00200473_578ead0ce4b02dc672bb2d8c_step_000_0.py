import cadquery as cq

# --- Parametric Dimensions ---
# Fuselage
fuselage_length = 60.0
fuselage_radius = 3.5
nose_length = 18.0

# Main Wings
wing_span = 42.0  # Semi-span
wing_root_chord = 18.0
wing_tip_chord = 8.0
wing_sweep = 12.0  # Longitudinal offset of tip relative to root
wing_root_x = 5.0  # LE position of root
wing_thickness_root = 2.0
wing_thickness_tip = 1.0

# Winglets
winglet_height = 8.0
winglet_root_chord = 8.0
winglet_tip_chord = 4.0
winglet_sweep = 4.0

# Tail
v_tail_height = 14.0
v_tail_root_chord = 12.0
v_tail_tip_chord = 6.0
v_tail_sweep = 6.0
v_tail_x = -22.0

h_tail_span = 14.0
h_tail_root_chord = 10.0
h_tail_tip_chord = 5.0
h_tail_sweep = 5.0
h_tail_x = -22.0

# --- Helper Functions ---

def get_airfoil_points(chord, thickness, x_offset=0, y_offset=0):
    """
    Returns a list of points (x, y) for a symmetric streamlined profile.
    Coordinates are relative to the given offsets.
    """
    pts = [
        (x_offset, y_offset),
        (x_offset + chord * 0.3, y_offset + thickness / 2.0),
        (x_offset + chord * 0.7, y_offset + thickness / 3.0),
        (x_offset + chord, y_offset),
        (x_offset + chord * 0.7, y_offset - thickness / 3.0),
        (x_offset + chord * 0.3, y_offset - thickness / 2.0),
        (x_offset, y_offset)
    ]
    return pts

# --- Geometry Construction ---

# 1. Fuselage Body and Nose
# Cylinder from X = -fuselage_length/2 to X = fuselage_length/2 approx
# Adjusted to position wing appropriately
fus_start = -fuselage_length + 20
fus_end = 20
fuselage = cq.Workplane("YZ").circle(fuselage_radius).extrude(fus_end - fus_start)
fuselage = fuselage.translate((fus_start, 0, 0))

# Nose Cone
nose = cq.Workplane("YZ").workplane(offset=fus_end).circle(fuselage_radius)\
    .workplane(offset=nose_length).circle(0.01).loft()

body = fuselage.union(nose)

# 2. Main Right Wing
# Defined on XZ planes, lofted along Y
# Embed root slightly into fuselage for clean union
root_offset_y = fuselage_radius * 0.8
tip_offset_y = root_offset_y + wing_span

# Calculate absolute coordinates for XZ plane spline
pts_wing_root = get_airfoil_points(wing_root_chord, wing_thickness_root, x_offset=wing_root_x, y_offset=0)
pts_wing_tip = get_airfoil_points(wing_tip_chord, wing_thickness_tip, x_offset=wing_root_x - wing_sweep, y_offset=0)

right_wing = (
    cq.Workplane("XZ")
    .workplane(offset=root_offset_y)
    .spline(pts_wing_root).close()
    .workplane(offset=wing_span)
    .spline(pts_wing_tip).close()
    .loft()
)

# 3. Right Winglet
# Vertical fin attached to the wing tip
# Defined on XY planes (horizontal sections), lofted along Z
wl_root_y = tip_offset_y
wl_root_x = wing_root_x - wing_sweep
wl_tip_x = wl_root_x - winglet_sweep

# Points are (x, y) where y is local "thickness" of the fin
# But we map them to (x, y) on the global plane. 
# For vertical fin, "thickness" is along Y axis of the profile, which maps to global Y? No.
# Vertical fin thickness is along Y global. Chord is along X global. Height is along Z.
# So we define profiles in XY plane.
# Root profile at Z=0 (approx wing tip level)
pts_wl_root = get_airfoil_points(winglet_root_chord, wing_thickness_tip, x_offset=wl_root_x, y_offset=wl_root_y)
# Tip profile at Z=winglet_height
pts_wl_tip = get_airfoil_points(winglet_tip_chord, wing_thickness_tip * 0.5, x_offset=wl_tip_x, y_offset=wl_root_y)

right_winglet = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .spline(pts_wl_root).close()
    .workplane(offset=winglet_height)
    .spline(pts_wl_tip).close()
    .loft()
)

# 4. Vertical Tail
# On top of fuselage rear
vt_pts_root = get_airfoil_points(v_tail_root_chord, fuselage_radius, x_offset=v_tail_x, y_offset=0)
vt_pts_tip = get_airfoil_points(v_tail_tip_chord, wing_thickness_tip, x_offset=v_tail_x - v_tail_sweep, y_offset=0)

# Note: Using y_offset=0 for profile centers it on Y axis
v_tail = (
    cq.Workplane("XY")
    .workplane(offset=fuselage_radius * 0.9)
    .spline(vt_pts_root).close()
    .workplane(offset=v_tail_height)
    .spline(vt_pts_tip).close()
    .loft()
)

# 5. Horizontal Tail (Right)
ht_pts_root = get_airfoil_points(h_tail_root_chord, wing_thickness_root, x_offset=h_tail_x, y_offset=0)
ht_pts_tip = get_airfoil_points(h_tail_tip_chord, wing_thickness_tip, x_offset=h_tail_x - h_tail_sweep, y_offset=0)

right_h_tail = (
    cq.Workplane("XZ")
    .workplane(offset=root_offset_y)
    .spline(ht_pts_root).close()
    .workplane(offset=h_tail_span)
    .spline(ht_pts_tip).close()
    .loft()
)

# --- Assembly and Mirroring ---

# Mirror right components to left
left_wing = right_wing.mirror("XZ")
left_winglet = right_winglet.mirror("XZ")
left_h_tail = right_h_tail.mirror("XZ")

# Combine all
result = (
    body
    .union(right_wing)
    .union(left_wing)
    .union(right_winglet)
    .union(left_winglet)
    .union(v_tail)
    .union(right_h_tail)
    .union(left_h_tail)
)