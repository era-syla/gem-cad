import cadquery as cq

# --- Parametric Dimensions ---
# Overall dimensions of the rectangular bar
bar_length = 150.0
bar_width = 30.0
bar_thickness = 10.0

# Hole dimensions
circle_diameter = 6.0
square_side = 6.0

# Positioning of the holes
# Distance from the center of the bar to the center of the hole groups
group_offset_from_center = 50.0  # (150/2) - (distance from edge to center of group) approx 25? Let's guess 50.
# Actually, looking at the image, the groups are near the ends.
# Let's say the groups are centered at +/- 50mm from the origin (assuming 150mm total length).

# Inside each group:
# Center-to-center spacing between the holes in a group
hole_spacing = 10.0

# --- Geometry Construction ---

# 1. Create the main rectangular body centered at the origin
result = cq.Workplane("XY").box(bar_length, bar_width, bar_thickness)

# 2. Create the hole locations
# We have two groups. 
# Group 1 (Left): Center at (-group_offset_from_center, 0)
#   - Circle hole: (-group_offset_from_center - hole_spacing, 0)
#   - Square hole: (-group_offset_from_center, 0)
#   - Circle hole: (-group_offset_from_center + hole_spacing, 0)
# Group 2 (Right): Center at (+group_offset_from_center, 0)
#   - Circle hole: (group_offset_from_center - hole_spacing, 0)
#   - Square hole: (group_offset_from_center, 0)
#   - Circle hole: (group_offset_from_center + hole_spacing, 0)

# Let's define the points relative to the main coordinate system
# Group centers
x_left = -group_offset_from_center
x_right = group_offset_from_center

# Points for circular holes
circle_points = [
    (x_left - hole_spacing, 0),
    (x_left + hole_spacing, 0),
    (x_right - hole_spacing, 0),
    (x_right + hole_spacing, 0)
]

# Points for square holes
square_points = [
    (x_left, 0),
    (x_right, 0)
]

# 3. Cut the circular holes
result = result.faces(">Z").workplane().pushPoints(circle_points).hole(circle_diameter)

# 4. Cut the square holes
# CadQuery's rect() creates a rectangle on the workplane stack. 
# We push the points, then draw rectangles, then cut them through.
result = result.faces(">Z").workplane().pushPoints(square_points).rect(square_side, square_side).cutThruAll()

# Depending on exact visual alignment, the spacing might be adjusted, 
# but this topology matches the image: 
# [Circle - Square - Circle] ----- [Circle - Square - Circle]