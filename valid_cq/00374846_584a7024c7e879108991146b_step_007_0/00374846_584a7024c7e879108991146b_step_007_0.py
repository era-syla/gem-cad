import cadquery as cq

# Parameter definitions for dimensions and features
plate_length = 200.0
plate_width = 150.0
plate_thickness = 4.0

hole_diameter = 8.0
edge_margin_x = 15.0  # Margin from the short edges
edge_margin_y = 15.0  # Margin from the long edges

count_holes_front = 6  # Number of holes on the front row (bottom in image)
count_holes_back = 5   # Number of holes on the back row (top in image)

# Create the base rectangular plate centered on XY plane
result = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# List to store hole coordinates
hole_points = []

# Calculate positions for the front row of holes (6 holes)
# This row is located along the negative Y side
y_pos_front = -(plate_width / 2) + edge_margin_y
x_start = -(plate_length / 2) + edge_margin_x
x_end = (plate_length / 2) - edge_margin_x
x_span = x_end - x_start

if count_holes_front > 1:
    step = x_span / (count_holes_front - 1)
    for i in range(count_holes_front):
        hole_points.append((x_start + (i * step), y_pos_front))

# Calculate positions for the back row of holes (5 holes)
# This row is located along the positive Y side
y_pos_back = (plate_width / 2) - edge_margin_y

if count_holes_back > 1:
    step = x_span / (count_holes_back - 1)
    for i in range(count_holes_back):
        hole_points.append((x_start + (i * step), y_pos_back))

# Create the holes using the calculated points
result = result.faces(">Z").workplane().pushPoints(hole_points).hole(hole_diameter)