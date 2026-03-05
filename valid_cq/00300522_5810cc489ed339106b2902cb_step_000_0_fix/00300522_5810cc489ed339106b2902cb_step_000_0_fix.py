import cadquery as cq

finger_count = 3
step_depth = 10
segment_height = 10
length = 200
thickness = 10

# Number of segments (twice the number of fingers)
seg_count = 2 * finger_count
bounds = range(seg_count + 1)

# Compute Z levels
z_coords = [i * segment_height for i in bounds]

# Offsets on the right (male fingers) at odd segments
offset_right = [step_depth if i % 2 == 1 else 0 for i in bounds]
# Offsets on the left (female slots) at even segments except top and bottom
offset_left = [
    step_depth if (i % 2 == 0 and i not in (0, seg_count)) else 0
    for i in bounds
]

# Compute Y positions for left and right edges at each Z
y_left = [offset_left[i] for i in bounds]
y_right = [length + offset_right[i] for i in bounds]

# Build the 2D profile in the YZ plane
points = []
# Start at bottom-left
points.append((y_left[0], z_coords[0]))
# Bottom-right
points.append((y_right[0], z_coords[0]))
# Right side upwards
for i in bounds[1:]:
    points.append((y_right[i], z_coords[i]))
# Top-left
points.append((y_left[-1], z_coords[-1]))
# Left side downwards
for i in reversed(bounds[1:-1]):
    points.append((y_left[i], z_coords[i]))

# Create the solid by extruding the profile in the X direction
result = (
    cq.Workplane("YZ")
    .polyline(points)
    .close()
    .extrude(thickness)
)