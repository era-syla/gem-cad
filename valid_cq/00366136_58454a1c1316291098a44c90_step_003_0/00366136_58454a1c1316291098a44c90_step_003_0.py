import cadquery as cq

# -- Parametric Dimensions --
tooth_width = 8.0        # Width of each tooth (and gap)
tooth_depth = 4.0        # Depth of the notches from the outer edge
plate_thickness = 3.0    # Thickness of the plate Z-axis
num_teeth_length = 18    # Number of teeth along the long side
num_teeth_width = 12     # Number of teeth along the short side

# -- Derived Dimensions --
# Total outer dimensions calculated to ensure corners are solid teeth
# Formula: (N_teeth * width) + (N_gaps * width), where N_gaps = N_teeth - 1
total_length = (2 * num_teeth_length - 1) * tooth_width
total_width = (2 * num_teeth_width - 1) * tooth_width

# -- Model Generation --

# 1. Create the base solid block representing the maximum outer bounds
result = cq.Workplane("XY").box(total_length, total_width, plate_thickness)

# 2. Define cutting operations for Top and Bottom edges (X-axis)
# We cut out the gaps between the teeth.
cut_points_x = []
x_start = -total_length / 2.0
y_pos_top = total_width / 2.0
y_pos_bottom = -total_width / 2.0

# Calculate centers of gaps along the X axis
for i in range(num_teeth_length - 1):
    # Gap i starts at: x_start + tooth_width + i * (tooth_width + gap_width)
    # Center is + 0.5 * gap_width
    gap_center_x = x_start + (2 * i + 1.5) * tooth_width
    cut_points_x.append((gap_center_x, y_pos_top))
    cut_points_x.append((gap_center_x, y_pos_bottom))

# Execute X-axis cuts
if cut_points_x:
    result = (
        result.faces(">Z").workplane()
        .pushPoints(cut_points_x)
        .rect(tooth_width, tooth_depth * 2)
        .cutThruAll()
    )

# 3. Define cutting operations for Left and Right edges (Y-axis)
cut_points_y = []
y_start = -total_width / 2.0
x_pos_right = total_length / 2.0
x_pos_left = -total_length / 2.0

# Calculate centers of gaps along the Y axis
for i in range(num_teeth_width - 1):
    gap_center_y = y_start + (2 * i + 1.5) * tooth_width
    cut_points_y.append((x_pos_right, gap_center_y))
    cut_points_y.append((x_pos_left, gap_center_y))

# Execute Y-axis cuts
if cut_points_y:
    result = (
        result.faces(">Z").workplane()
        .pushPoints(cut_points_y)
        .rect(tooth_depth * 2, tooth_width)
        .cutThruAll()
    )