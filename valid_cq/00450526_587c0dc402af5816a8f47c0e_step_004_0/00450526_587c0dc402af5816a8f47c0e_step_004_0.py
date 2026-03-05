import cadquery as cq
import math

# --- Parameters ---

# Main Body Dimensions
body_length = 100.0
body_width_top = 40.0
body_width_bottom = 12.0
body_height_side = 22.0  # Height of the straight side walls before the curve starts (approx)
# Actually, defining by total profile height and radius is better
body_height_total = 25.0 # Height at the corners
top_radius = 35.0        # Radius of the top curved surface

# Boss Dimensions
boss_diameter = 26.0
boss_protrusion = 8.0    # Height boss sticks out above the center of the curve
boss_flat_width = 18.0   # Distance between flats

# Tab Dimensions
tab_size = 6.0
tab_length = 5.0

# --- Geometry Construction ---

# 1. Main Body
# Construct profile on YZ plane (Side View)
# We calculate the peak height of the arc to ensure geometry consistency

# Chord is the top width
half_chord = body_width_top / 2.0
# Calculate sagitta (height of the arc cap)
# h = R - sqrt(R^2 - (w/2)^2)
if top_radius < half_chord:
    top_radius = half_chord + 0.1 # constrain radius to be at least half width
    
sagitta = top_radius - math.sqrt(top_radius**2 - half_chord**2)
center_peak_z = body_height_total + sagitta

# Define points for the cross-section profile
# Coordinates are (Y, Z) in the local YZ plane
p_bottom_left = (-body_width_bottom / 2.0, 0.0)
p_bottom_right = (body_width_bottom / 2.0, 0.0)
p_top_right = (body_width_top / 2.0, body_height_total)
p_top_left = (-body_width_top / 2.0, body_height_total)
p_top_mid = (0.0, center_peak_z)

# Create the body by extruding the sketch along X (both directions to center on origin)
main_body = (
    cq.Workplane("YZ")
    .moveTo(*p_bottom_left)
    .lineTo(*p_bottom_right)
    .lineTo(*p_top_right)
    .threePointArc(p_top_mid, p_top_left)
    .close()
    .extrude(body_length / 2.0, both=True)
)

# 2. Top Boss
# Calculate total height for boss extrusion
boss_z_top = center_peak_z + boss_protrusion

# Create the base cylinder for the boss
boss_raw = (
    cq.Workplane("XY")
    .circle(boss_diameter / 2.0)
    .extrude(boss_z_top)
)

# Cut the flats on the boss
# We create cutters that remove material outside the flat_width
cutter_width = boss_diameter # Sufficient width to clear the circle
cutter_offset = (boss_flat_width / 2.0) + (cutter_width / 2.0)

boss_cutters = (
    cq.Workplane("XY")
    # Cutter 1 (Positive Y)
    .moveTo(0, cutter_offset)
    .rect(boss_diameter * 2, cutter_width)
    # Cutter 2 (Negative Y)
    .moveTo(0, -cutter_offset)
    .rect(boss_diameter * 2, cutter_width)
    .extrude(boss_z_top + 1.0) # Extrude slightly higher to ensure cut
)

# Apply cut to boss
boss_final = boss_raw.cut(boss_cutters)

# 3. End Tab
# Create a square tab on the positive X face at the bottom
tab = (
    cq.Workplane("YZ")
    .workplane(offset=body_length / 2.0)
    .moveTo(0, tab_size / 2.0) # Center the square on Y=0, Z=tab_size/2 (resting on bottom)
    .rect(tab_size, tab_size)
    .extrude(tab_length)
)

# --- Final Assembly ---
result = main_body.union(boss_final).union(tab)