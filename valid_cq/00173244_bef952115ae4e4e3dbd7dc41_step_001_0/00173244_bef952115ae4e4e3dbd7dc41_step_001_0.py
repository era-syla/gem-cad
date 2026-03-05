import cadquery as cq

# --- Parameters ---

# Plate dimensions
plate_thickness = 3.0
plate_height = 80.0
plate_bottom_width = 260.0

# Trapezoid shape definition (X coordinates of top corners relative to origin)
# Origin is at the bottom-left corner of the plate
plate_top_left_x = 50.0
plate_top_right_x = 170.0

# Rectangular cutout dimensions
cutout_width = 40.0
cutout_height = 24.0
cutout_gap = 30.0  # Space between the two rectangular cutouts

# Mounting hole parameters
hole_diameter = 3.2
hole_margin = 4.5  # Distance from the edge of the rectangle to the center of the hole

# Positioning calculations
# Calculate vertical center
center_y = plate_height / 2.0

# Calculate horizontal center for the cutout group
# Roughly centering based on the mid-height width of the trapezoid
mid_height_left_x = plate_top_left_x / 2.0
mid_height_right_x = plate_bottom_width - ((plate_bottom_width - plate_top_right_x) / 2.0)
center_x = (mid_height_left_x + mid_height_right_x) / 2.0

# Calculate center points for the two rectangles
dist_from_center = (cutout_width + cutout_gap) / 2.0
rect_centers = [
    (center_x - dist_from_center, center_y),
    (center_x + dist_from_center, center_y)
]

# Calculate relative offsets for the mounting holes
hole_offset_x = (cutout_width / 2.0) + hole_margin
hole_offset_y = (cutout_height / 2.0) + hole_margin

# --- 3D Modeling ---

# 1. Create the base trapezoidal plate
points = [
    (0, 0),
    (plate_bottom_width, 0),
    (plate_top_right_x, plate_height),
    (plate_top_left_x, plate_height)
]

result = (
    cq.Workplane("XY")
    .polyline(points + [points[0]])
    .close()
    .extrude(plate_thickness)
)

# 2. Create the rectangular cutouts
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(rect_centers)
    .rect(cutout_width, cutout_height)
    .cutThruAll()
)

# 3. Create the mounting holes
# Generate coordinates for all 8 holes
hole_points = []
for (rc_x, rc_y) in rect_centers:
    hole_points.extend([
        (rc_x - hole_offset_x, rc_y - hole_offset_y),
        (rc_x + hole_offset_x, rc_y - hole_offset_y),
        (rc_x + hole_offset_x, rc_y + hole_offset_y),
        (rc_x - hole_offset_x, rc_y + hole_offset_y)
    ])

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(hole_points)
    .circle(hole_diameter / 2.0)
    .cutThruAll()
)