import cadquery as cq

# -- Parametric Dimensions --
width = 100.0          # Total width of the plate
height = 60.0          # Total height of the plate
thickness = 5.0        # Plate thickness

# Side Finger Joint details
# The side is divided into 5 vertical segments: Tab-Notch-Tab-Notch-Tab
num_vertical_segments = 5
segment_height = height / num_vertical_segments
side_notch_depth = 5.0 # Depth of the side cutouts (horizontal)

# Bottom Notch details
bottom_notch_depth = 5.0
bottom_notch_width = 20.0
corner_foot_width = 15.0 # Width of the solid feet at the bottom corners

# -- Geometry Construction --

# Initialize a Sketch
# We start with the full bounding rectangle and subtract the notches (mode='s')
sketch = cq.Sketch().rect(width, height)

# 1. Side Notches
# We identify the vertical centers for the 2nd and 4th segments (indices 1 and 3)
# Y-coordinates relative to the center (0,0)
y_pos_notch_1 = -height/2 + (1.5 * segment_height)
y_pos_notch_2 = -height/2 + (3.5 * segment_height)

# Cutter dimensions for side notches
# Width is doubled and centered on the edge to ensure a clean cut of 'side_notch_depth'
side_cutter_w = side_notch_depth * 2
side_cutter_h = segment_height

# Cut Left Side
sketch = (
    sketch
    .push([(-width/2, y_pos_notch_1), (-width/2, y_pos_notch_2)])
    .rect(side_cutter_w, side_cutter_h, mode='s')
)

# Cut Right Side
sketch = (
    sketch
    .push([(width/2, y_pos_notch_1), (width/2, y_pos_notch_2)])
    .rect(side_cutter_w, side_cutter_h, mode='s')
)

# 2. Bottom Notches
# Calculate X positions relative to center
# Center of left notch = Left Edge + Corner Foot Width + Half Notch Width
x_pos_left = -width/2 + corner_foot_width + bottom_notch_width/2
# Center of right notch = Symmetric
x_pos_right = width/2 - corner_foot_width - bottom_notch_width/2

# Cutter dimensions for bottom notches
# Height is doubled and centered on the bottom edge
bottom_cutter_w = bottom_notch_width
bottom_cutter_h = bottom_notch_depth * 2

sketch = (
    sketch
    .push([(x_pos_left, -height/2), (x_pos_right, -height/2)])
    .rect(bottom_cutter_w, bottom_cutter_h, mode='s')
)

# 3. Create 3D Solid
# Extrude the final profile
result = cq.Workplane("XY").placeSketch(sketch).extrude(thickness)