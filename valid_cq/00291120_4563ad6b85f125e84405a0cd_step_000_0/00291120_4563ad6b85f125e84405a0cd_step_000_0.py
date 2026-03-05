import cadquery as cq

# --- Parametric Dimensions ---
# Overall dimensions of the bar
length = 120.0
height = 15.0
thickness = 6.0

# Nose feature dimensions (the leading end)
nose_vertical_height = 5.0  # Height of the vertical face at the very front
nose_ramp_length = 8.0      # Horizontal length of the sloped section

# Notch/Tooth dimensions
notch_depth = 4.0
notch_top_width = 7.0
notch_bottom_width = 2.0
land_length = 6.0           # Length of the flat top section between features
number_of_notches = 2

# Calculated dimensions
notch_slope_run = (notch_top_width - notch_bottom_width) / 2.0

# --- Geometry Definition ---

# Define the profile points starting from the bottom-left corner (0,0)
points = []

# 1. Start at origin
points.append((0, 0))

# 2. Front vertical face
points.append((0, nose_vertical_height))

# 3. Nose ramp (sloping up to full height)
current_x = nose_ramp_length
points.append((current_x, height))

# 4. Generate notches and lands
for _ in range(number_of_notches):
    # Flat Land
    current_x += land_length
    points.append((current_x, height))
    
    # Notch Down-Slope
    current_x += notch_slope_run
    points.append((current_x, height - notch_depth))
    
    # Notch Bottom
    current_x += notch_bottom_width
    points.append((current_x, height - notch_depth))
    
    # Notch Up-Slope
    current_x += notch_slope_run
    points.append((current_x, height))

# 5. Top edge to the back of the part
points.append((length, height))

# 6. Back vertical face
points.append((length, 0))

# 7. Close the loop back to origin
points.append((0, 0))

# --- Solid Generation ---
result = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(thickness)
)