import cadquery as cq

# Parameters for the robot chassis plate
plate_thickness = 3.0
plate_width = 120.0  # Overall width of the circular part
total_length = 200.0 # Approximate total length
circle_radius = plate_width / 2.0

# Rectangular tail section parameters
tail_width = 80.0
tail_length = 100.0
tail_corner_chamfer = 10.0

# Motor/Wheel cutouts (the two large rectangles)
cutout_width = 25.0
cutout_length = 50.0
cutout_spacing = 15.0 # Distance between the two cutouts
cutout_center_y = -30.0 # Position relative to the center of the circle

# Mounting holes
hole_diameter = 3.5
hole_offset_x = tail_width / 2 - 8.0 # Distance from centerline
hole_y_positions = [-20.0, -90.0] # Y positions relative to circle center

# Create the base shape
# We'll construct this by unioning a circle and a rectangle, then cutting away parts
# 1. Start with the circular front section
front_circle = cq.Workplane("XY").circle(circle_radius).extrude(plate_thickness)

# 2. Create the rectangular tail section
# Center of the rectangle needs to be positioned so it overlaps correctly
rect_center_y = -tail_length / 2
tail_rect = (
    cq.Workplane("XY")
    .center(0, rect_center_y)
    .rect(tail_width, tail_length)
    .extrude(plate_thickness)
)

# 3. Combine the circle and rectangle
combined_plate = front_circle.union(tail_rect)

# 4. Refine the shape: Apply chamfers to the bottom corners of the tail
# We need to select vertical edges at the very back (lowest Y)
final_shape = (
    combined_plate
    .edges(f"|Z and <Y") # Select vertical edges at the minimum Y
    .chamfer(tail_corner_chamfer)
)

# 5. Create the rectangular cutouts
# We need two rectangles centered around the Y-axis
left_cutout = (
    cq.Workplane("XY")
    .center(-cutout_width/2 - cutout_spacing/2, cutout_center_y)
    .rect(cutout_width, cutout_length)
    .extrude(plate_thickness * 2) # Make sure it cuts through
    .translate((0, 0, -plate_thickness/2)) # Center vertically
)

right_cutout = (
    cq.Workplane("XY")
    .center(cutout_width/2 + cutout_spacing/2, cutout_center_y)
    .rect(cutout_width, cutout_length)
    .extrude(plate_thickness * 2)
    .translate((0, 0, -plate_thickness/2))
)

# Apply cutouts
result = final_shape.cut(left_cutout).cut(right_cutout)

# 6. Create mounting holes
# We can define points and drill all at once
hole_points = [
    (hole_offset_x, hole_y_positions[0]),
    (-hole_offset_x, hole_y_positions[0]),
    (hole_offset_x, hole_y_positions[1]),
    (-hole_offset_x, hole_y_positions[1]),
]

result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(hole_points)
    .hole(hole_diameter)
)