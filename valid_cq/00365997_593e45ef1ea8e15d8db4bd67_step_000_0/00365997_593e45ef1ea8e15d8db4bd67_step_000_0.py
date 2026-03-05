import cadquery as cq

# --- Parameters ---

# Main body dimensions
plate_width = 100.0
plate_height = 60.0
plate_thickness = 4.0

# Side notches (left and right edges)
side_notch_depth = 4.0
side_notch_height = 8.0
side_notch_y_offset = -5.0  # Offset from the horizontal center line

# Bottom notches
bottom_notch_width = 15.0
bottom_notch_depth = 5.0
bottom_notch_spacing = 45.0 # Center-to-center distance between bottom notches

# Large rectangular cutout (top right)
large_cutout_w = 10.0
large_cutout_h = 16.0
large_cutout_center_x = 35.0
large_cutout_center_y = 12.0

# Hole pattern parameters
hole_pitch = 9.0
hole_start_x = -40.0
circle_row_y = -2.0
square_row_y = -14.0
circle_diameter = 4.0
square_size = 4.0
num_circles = 8
num_squares = 7

# --- Modeling ---

# 1. Create the base plate
result = cq.Workplane("XY").box(plate_width, plate_height, plate_thickness)

# 2. Cut Side Notches
# We place rectangles centered on the left and right edges.
# Width is doubled so the center can be on the edge while cutting the full depth.
result = (
    result.faces("Z")
    .workplane()
    .pushPoints([
        (-plate_width / 2, side_notch_y_offset), 
        (plate_width / 2, side_notch_y_offset)
    ])
    .rect(side_notch_depth * 2, side_notch_height)
    .cutThruAll()
)

# 3. Cut Bottom Notches
# We place rectangles centered on the bottom edge.
# Height is doubled to cut depth into the plate from the edge.
result = (
    result.faces("Z")
    .workplane()
    .pushPoints([
        (-bottom_notch_spacing / 2, -plate_height / 2),
        (bottom_notch_spacing / 2, -plate_height / 2)
    ])
    .rect(bottom_notch_width, bottom_notch_depth * 2)
    .cutThruAll()
)

# 4. Cut Large Rectangular Window
result = (
    result.faces("Z")
    .workplane()
    .moveTo(large_cutout_center_x, large_cutout_center_y)
    .rect(large_cutout_w, large_cutout_h)
    .cutThruAll()
)

# 5. Cut Circular Holes Row
circle_points = [(hole_start_x + i * hole_pitch, circle_row_y) for i in range(num_circles)]
result = (
    result.faces("Z")
    .workplane()
    .pushPoints(circle_points)
    .circle(circle_diameter / 2)
    .cutThruAll()
)

# 6. Cut Square Holes Row
square_points = [(hole_start_x + i * hole_pitch, square_row_y) for i in range(num_squares)]
result = (
    result.faces("Z")
    .workplane()
    .pushPoints(square_points)
    .rect(square_size, square_size)
    .cutThruAll()
)