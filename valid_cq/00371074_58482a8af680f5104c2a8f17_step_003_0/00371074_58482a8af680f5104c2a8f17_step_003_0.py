import cadquery as cq
import math

# --- Parameters ---
# Overall Dimensions
width = 400.0
height = 250.0
thickness = 2.0
frame_width = 30.0

# Feature Dimensions
# Corner notches (located at the bottom corners of the inner cutout)
corner_notch_w = 12.0  # Depth of the cut into the frame width
corner_notch_h = 25.0  # Height of the notch along the vertical edge

# Mid-side notches (located at the center of the vertical edges)
mid_notch_d = 4.0     # Depth of the cut into the frame width
mid_notch_h = 10.0    # Height of the notch

# Hole Pattern
hole_diameter = 3.5
num_holes_top = 9     # Number of holes along the top edge
num_holes_side = 6    # Number of holes along the side edge

# --- Geometry Construction ---

# 1. Define the Basic Solids
# Outer boundary rectangle extruded
outer_solid = cq.Workplane("XY").rect(width, height).extrude(thickness)

# 2. Define the Inner Cutout Profile
# We construct the complex inner shape using a polyline point list.
# Dimensions of the nominal inner rectangle
iw = width - 2 * frame_width
ih = height - 2 * frame_width
half_iw = iw / 2.0
half_ih = ih / 2.0

# Define points clockwise starting from Top-Left
# Coordinates are relative to the center of the part
pts = []

# Top Left Corner
pts.append((-half_iw, half_ih))

# Top Right Corner
pts.append((half_iw, half_ih))

# Right Side: Mid Notch
pts.append((half_iw, mid_notch_h / 2.0))
pts.append((half_iw + mid_notch_d, mid_notch_h / 2.0))
pts.append((half_iw + mid_notch_d, -mid_notch_h / 2.0))
pts.append((half_iw, -mid_notch_h / 2.0))

# Right Side: Bottom Corner Notch
pts.append((half_iw, -half_ih + corner_notch_h))
pts.append((half_iw + corner_notch_w, -half_ih + corner_notch_h))
pts.append((half_iw + corner_notch_w, -half_ih))

# Bottom Edge (Connects the two extended bottom corners)
pts.append((-half_iw - corner_notch_w, -half_ih))

# Left Side: Bottom Corner Notch
pts.append((-half_iw - corner_notch_w, -half_ih + corner_notch_h))
pts.append((-half_iw, -half_ih + corner_notch_h))

# Left Side: Mid Notch
pts.append((-half_iw, -mid_notch_h / 2.0))
pts.append((-half_iw - mid_notch_d, -mid_notch_h / 2.0))
pts.append((-half_iw - mid_notch_d, mid_notch_h / 2.0))
pts.append((-half_iw, mid_notch_h / 2.0))

# Create the cutout solid
cutout_solid = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(thickness)
)

# 3. Create the Frame
# Subtract the inner cutout from the outer block
result = outer_solid.cut(cutout_solid)

# 4. Add Holes
# We distribute holes along the centerline of the frame strips
cl_width = width - frame_width   # Centerline width
cl_height = height - frame_width # Centerline height
hx = cl_width / 2.0
hy = cl_height / 2.0

hole_pts = []

# Top and Bottom Rows (Linear spacing)
# We generate equidistant points along the X axis
if num_holes_top > 1:
    step_x = cl_width / (num_holes_top - 1)
    for i in range(num_holes_top):
        x = -hx + i * step_x
        hole_pts.append((x, hy))  # Top row hole
        hole_pts.append((x, -hy)) # Bottom row hole
else:
    # Fallback for single hole
    hole_pts.append((0, hy))
    hole_pts.append((0, -hy))

# Side Columns
# We generate points along the Y axis
# Note: We exclude the first and last points if they overlap with the corners 
# created by the top/bottom rows.
if num_holes_side > 2:
    step_y = cl_height / (num_holes_side - 1)
    # Range is 1 to N-2 to skip the corners at index 0 and N-1
    for i in range(1, num_holes_side - 1):
        y = -hy + i * step_y
        hole_pts.append((hx, y))   # Right column hole
        hole_pts.append((-hx, y))  # Left column hole

# Drill the holes
result = result.faces(">Z").workplane().pushPoints(hole_pts).hole(hole_diameter)