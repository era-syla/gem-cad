import cadquery as cq
import math

# --- Parameters ---
length = 600.0
height_left = 100.0
height_right = 220.0
thickness = 10.0
chamfer_right = 120.0

# Notch parameters
notch_width = 40.0
notch_top_y = -60.0  # Y coordinate of the top of the notch (relative to top edge)
notch1_x = 220.0
notch2_x = 340.0

# Hole diameters
d_small = 6.0
d_med = 12.0
d_large = 25.0

# --- Geometry Construction ---

# 1. Base Plate Shape
# Defined by 4 points creating a trapezoid-like shape
# Top edge lies on the X-axis (Y=0)
pts = [
    (0, 0),                          # Top-Left
    (length, 0),                     # Top-Right
    (length - chamfer_right, -height_right), # Bottom-Right
    (0, -height_left)                # Bottom-Left
]

result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(thickness)
)

# 2. Cut Rectangular Notches
# We position a tall cutting tool such that its top edge aligns with notch_top_y
notch_height_tool = 500.0
notch_y_center = notch_top_y - (notch_height_tool / 2.0)

notch_locations = [
    (notch1_x, notch_y_center),
    (notch2_x, notch_y_center)
]

result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(notch_locations)
    .rect(notch_width, notch_height_tool)
    .cutThruAll()
)

# 3. Create Hole Patterns

# Define point coordinates
# Left tip triangle pattern
left_holes = [(25, -25), (25, -65), (55, -45)]

# Single hole near top center
top_hole = [(280, -25)]

# Vertical column between notches
center_col_holes = [(280, -80), (280, -100), (280, -120)]

# Bearing area (Large hole + ring of small holes)
bearing_center_pt = (460, -120)
bearing_radius = 45.0

# Generate ring points
bearing_ring_holes = []
for i in range(6):
    angle = math.radians(i * 60)
    bx = bearing_center_pt[0] + bearing_radius * math.cos(angle)
    by = bearing_center_pt[1] + bearing_radius * math.sin(angle)
    bearing_ring_holes.append((bx, by))

# Right tip triangle pattern
right_tip_holes = [(560, -140), (580, -160), (560, -180)]

# Miscellaneous scattered holes
scattered_holes = [(400, -160), (490, -190)]

# Combine all small hole locations
small_holes = (
    left_holes + 
    center_col_holes + 
    bearing_ring_holes + 
    right_tip_holes + 
    scattered_holes
)

# 4. Cut Holes
result = (
    result
    .faces(">Z")
    .workplane()
    # Cut small holes
    .pushPoints(small_holes)
    .circle(d_small / 2.0)
    .cutThruAll()
    # Cut medium hole
    .pushPoints(top_hole)
    .circle(d_med / 2.0)
    .cutThruAll()
    # Cut large bearing hole
    .pushPoints([bearing_center_pt])
    .circle(d_large / 2.0)
    .cutThruAll()
)