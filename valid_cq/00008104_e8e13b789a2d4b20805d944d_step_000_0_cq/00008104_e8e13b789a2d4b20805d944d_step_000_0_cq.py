import cadquery as cq

# Parametric dimensions
length = 1000.0  # Total length of the bar
height = 50.0    # Height of the bar
thickness = 5.0  # Thickness of the bar

# Hole configuration
hole_diameter = 4.0
# The image shows pairs of holes distributed along the length.
# Let's approximate the pattern based on the visual evidence.
# There appear to be pairs at the ends and spaced along the middle.
# Vertical spacing of hole pairs:
hole_vertical_spacing = 30.0 

# Horizontal positions for the hole pairs (relative to center)
# The image shows roughly 5 or 6 pairs. Let's assume symmetric placement.
# Let's create a list of X-coordinates for the hole columns.
# Assuming a symmetric distribution from center (0,0).
num_pairs = 6
x_spacing = length / num_pairs
x_positions = []

# Generate x positions centered around 0
start_x = -length/2 + x_spacing/2
for i in range(num_pairs):
    x_positions.append(start_x + i * x_spacing)

# Create the base rectangular bar
result = cq.Workplane("XY").box(length, height, thickness)

# Create the holes
# We need to iterate through the X positions and place two holes at each X
# One upper, one lower.
holes_pts = []

for x in x_positions:
    holes_pts.append((x, hole_vertical_spacing / 2))
    holes_pts.append((x, -hole_vertical_spacing / 2))

# There are also holes on the very ends (short edges) visible in the image.
# Let's add those specific end holes.
end_offset = 15.0 # Distance from the very edge
holes_pts.append((-length/2 + end_offset, hole_vertical_spacing / 2))
holes_pts.append((-length/2 + end_offset, -hole_vertical_spacing / 2))
holes_pts.append((length/2 - end_offset, hole_vertical_spacing / 2))
holes_pts.append((length/2 - end_offset, -hole_vertical_spacing / 2))

# Perform the cut operation
result = result.faces(">Z").workplane().pushPoints(holes_pts).hole(hole_diameter)

# Optional: Add the small holes on the end face (thickness side) seen on the left
# The image resolution is low, but there appear to be features on the small end face.
# Assuming tapped holes on the ends.
end_hole_dia = 3.0
result = (
    result.faces("<X").workplane()
    .pushPoints([(0, 10), (0, -10)]) # Adjust spacing as needed
    .hole(end_hole_dia, depth=15)
)

# Return result for visualization
# show_object(result)