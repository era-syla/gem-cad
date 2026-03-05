import cadquery as cq

# ------------------------------------------------------------------------------
# Parameters
# ------------------------------------------------------------------------------
# Define the dimensions of the gear rack / timing belt section
pitch = 2.0              # Distance between tooth centers (mm)
num_teeth = 100          # Total number of teeth
width = 6.0              # Width of the strip (mm)
base_thickness = 1.2     # Thickness of the solid belt/base below teeth (mm)
tooth_height = 1.0       # Height of the teeth (mm)
tooth_top_width = 0.8    # Width of the flat top of the tooth (mm)
tooth_base_width = 1.4   # Width of the tooth at the base (mm)

# ------------------------------------------------------------------------------
# Geometry Calculation
# ------------------------------------------------------------------------------
# Calculate total length
length = num_teeth * pitch

# Calculate spacing parameters for centering teeth in pitch
gap_margin = (pitch - tooth_base_width) / 2.0
slope_run = (tooth_base_width - tooth_top_width) / 2.0

# Define the points for the side profile on the YZ plane
# (Length along Y axis, Height along Z axis)
pts = []

# 1. Start at Origin (Bottom-Left of base)
pts.append((0, 0))

# 2. Bottom-Right of base
pts.append((length, 0))

# 3. Top-Right of base (Start of the tooth profile line)
pts.append((length, base_thickness))

# 4. Generate the zigzag tooth profile
# We iterate backwards from the last tooth to the first (Right to Left)
# to maintain a counter-clockwise winding order for the polyline.
for i in range(num_teeth - 1, -1, -1):
    # Start Y coordinate of the current pitch slot
    pitch_start_y = i * pitch
    
    # Calculate Y coordinates for the trapezoidal tooth profile
    # Order: Base Right -> Top Right -> Top Left -> Base Left
    y_base_right = pitch_start_y + pitch - gap_margin
    y_top_right  = y_base_right - slope_run
    y_top_left   = y_top_right - tooth_top_width
    y_base_left  = y_top_left - slope_run
    
    # Add points to the profile list
    pts.append((y_base_right, base_thickness))
    pts.append((y_top_right, base_thickness + tooth_height))
    pts.append((y_top_left, base_thickness + tooth_height))
    pts.append((y_base_left, base_thickness))

# 5. Top-Left of base (Close the profile back to the vertical edge)
pts.append((0, base_thickness))

# ------------------------------------------------------------------------------
# Solid Creation
# ------------------------------------------------------------------------------
# Create a sketch on the YZ plane and extrude along X (Width)
result = (
    cq.Workplane("YZ")
    .polyline(pts)
    .close()
    .extrude(width)
)