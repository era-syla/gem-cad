import cadquery as cq

# --- Parameters ---
length = 1600.0        # Total length of the frame
width = 400.0          # Total width (depth)
height = 400.0         # Total height
profile = 30.0         # Square tube profile size
side_bay_len = 450.0   # Length of the two side sections

# --- Calculations ---
# Half dimensions for centering
L_half = length / 2.0
W_half = width / 2.0
H_half = height / 2.0
p_half = profile / 2.0

# Define X coordinates for the structural "stations" (supports)
# Stations are centered on the profile width
x_start = -L_half + p_half
x_div1 = -L_half + side_bay_len
x_div2 = L_half - side_bay_len
x_end = L_half - p_half

stations = [x_start, x_div1, x_div2, x_end]

# Offset positions for rails
y_offset = W_half - p_half
z_offset = H_half - p_half

# Component Dimensions based on overlaps
# Verticals fit between top and bottom rails
post_height = height - (2 * profile)
# Crossbars fit between front and back rails
crossbar_width = width - (2 * profile)

# --- Geometry Construction ---

# 1. Define Primitives
# Longitudinal Rail (X-axis)
rail_shape = cq.Workplane("XY").box(length, profile, profile)

# Vertical Post (Z-axis)
post_shape = cq.Workplane("XY").box(profile, profile, post_height)

# Transverse Crossbar (Y-axis)
crossbar_shape = cq.Workplane("XY").box(profile, crossbar_width, profile)

parts = []

# 2. Place Long Rails (4 instances)
# Top-Front, Top-Back, Bottom-Front, Bottom-Back
for y_sign in [-1, 1]:
    for z_sign in [-1, 1]:
        pos = (0, y_sign * y_offset, z_sign * z_offset)
        parts.append(rail_shape.translate(pos))

# 3. Place Station Components (Verticals and Crossbars)
for x in stations:
    # Vertical Posts (Front and Back pairs)
    for y_sign in [-1, 1]:
        pos = (x, y_sign * y_offset, 0)
        parts.append(post_shape.translate(pos))
    
    # Crossbars (Top and Bottom pairs)
    for z_sign in [-1, 1]:
        pos = (x, 0, z_sign * z_offset)
        parts.append(crossbar_shape.translate(pos))

# 4. Combine into final solid
result = parts[0]
for part in parts[1:]:
    result = result.union(part)