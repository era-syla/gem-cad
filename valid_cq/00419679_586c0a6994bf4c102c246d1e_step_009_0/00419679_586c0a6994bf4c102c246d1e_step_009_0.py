import cadquery as cq

# --- Parametric Dimensions ---
height = 100.0
width_max = 40.0
width_neck = 20.0
thickness = 5.0

# Vertical section heights
h_top_block = 18.0
h_top_taper = 10.0
h_btm_taper = 10.0
h_btm_block = 25.0

# Notch dimensions (Triangle cut at bottom)
notch_height = 15.0
notch_width_base = 25.0

# Groove dimensions
groove_depth = 0.8
groove_width = 1.5
top_groove_y = height/2 - h_top_block  # Positioned at the top transition
btm_groove_offset = 6.0              # Positioned above the notch

# Hole dimensions
hole_diam = 2.0
hole_x_offset = 4.0
hole_y_offset = 4.0

# --- Geometry Construction ---

# 1. Define the 2D Profile (Right half, clockwise)
# Coordinates relative to center (0,0)
pts = []
y_top = height / 2.0
y_btm = -height / 2.0

# Top Center
pts.append((0, y_top))
# Top Right Corner
pts.append((width_max / 2.0, y_top))
# Top Block Side
pts.append((width_max / 2.0, y_top - h_top_block))
# Top Taper End (Start of Neck)
pts.append((width_neck / 2.0, y_top - h_top_block - h_top_taper))
# Bottom Taper Start (End of Neck)
# Calculate Y position based on bottom up dimensions
y_neck_btm = y_btm + h_btm_block + h_btm_taper
pts.append((width_neck / 2.0, y_neck_btm))
# Bottom Block Start (End of Taper)
pts.append((width_max / 2.0, y_btm + h_btm_block))
# Bottom Right Corner
pts.append((width_max / 2.0, y_btm))
# Notch Start on Bottom Edge
pts.append((notch_width_base / 2.0, y_btm))
# Notch Peak
pts.append((0, y_btm + notch_height))

# Generate Left Side via Mirroring
# Filter out points on X=0 axis to avoid duplicates, reverse order
left_pts = [(-p[0], p[1]) for p in reversed(pts) if p[0] > 1e-5]
profile_pts = pts + left_pts

# Extrude Main Body
result = cq.Workplane("XY").polyline(profile_pts).close().extrude(thickness)

# 2. Cut Top Horizontal Groove
result = (
    result.faces(">Z")
    .workplane(centerOption="ProjectedOrigin")
    .center(0, top_groove_y)
    .rect(width_max + 5.0, groove_width) # Extra width to ensure through-cut on sides
    .cutBlind(-groove_depth)
)

# 3. Cut Bottom V-Groove
# Calculate geometry parallel to the notch
groove_peak_y = y_btm + notch_height + btm_groove_offset

# Calculate slope of the notch: m = dy/dx
# Notch goes from (0, peak) to (width/2, bottom)
notch_slope = (y_btm - (y_btm + notch_height)) / (notch_width_base / 2.0)

# Calculate Y height of groove at the outer edge of the part
y_groove_edge = notch_slope * (width_max / 2.0) + groove_peak_y

# Define Polygon for V-Groove (Right Side Strip)
half_gw = groove_width / 2.0
v_poly_pts = [
    (0, groove_peak_y + half_gw),              # Peak Top
    (width_max/2.0, y_groove_edge + half_gw),  # Edge Top
    (width_max/2.0, y_groove_edge - half_gw),  # Edge Bottom
    (0, groove_peak_y - half_gw)               # Peak Bottom
]
# Mirror for Left Side
v_poly_left = [(-p[0], p[1]) for p in reversed(v_poly_pts) if p[0] > 1e-5]
full_v_poly = v_poly_pts + v_poly_left

result = (
    result.faces(">Z")
    .workplane(centerOption="ProjectedOrigin")
    .polyline(full_v_poly)
    .close()
    .cutBlind(-groove_depth)
)

# 4. Drill Mounting Hole
# Top Right corner location
h_x = width_max / 2.0 - hole_x_offset
h_y = y_top - hole_y_offset

result = (
    result.faces(">Z")
    .workplane(centerOption="ProjectedOrigin")
    .pushPoints([(h_x, h_y)])
    .hole(hole_diam)
)