import cadquery as cq

# Parameters for the trailer frame
frame_width = 200.0   # Width of the rectangular bed
frame_length = 300.0  # Length of the rectangular bed
tongue_length = 100.0 # Length of the triangular tongue extending from the front
tube_size = 10.0      # Width/Height of the square tubing
wall_thickness = 10.0 # Full solid bars are simpler, but let's assume solid for visual simplicity or parameterize for hollow

# Calculated parameters
half_width = frame_width / 2.0
num_cross_members = 4 # Includes front and back of the rectangle

# 1. Create the main rectangular frame outer loop
# We'll create the side rails first
left_rail = (
    cq.Workplane("XY")
    .box(tube_size, frame_length, tube_size)
    .translate((-half_width + tube_size/2, 0, 0))
)

right_rail = (
    cq.Workplane("XY")
    .box(tube_size, frame_length, tube_size)
    .translate((half_width - tube_size/2, 0, 0))
)

# 2. Create Cross Members
# Calculate spacing. We want members at start, end, and evenly spaced in between.
# The rails run the full length, so cross members fit between them.
cross_member_length = frame_width - (2 * tube_size)
spacing = (frame_length - tube_size) / (num_cross_members - 1)
start_y = -frame_length/2 + tube_size/2

cross_members = cq.Workplane("XY")

for i in range(num_cross_members):
    y_pos = start_y + (i * spacing)
    new_member = (
        cq.Workplane("XY")
        .box(cross_member_length, tube_size, tube_size)
        .translate((0, y_pos, 0))
    )
    cross_members = cross_members.union(new_member)

# 3. Create the Tongue (A-frame)
# The tongue consists of two angled beams meeting at a point, and a cross-brace.
# The triangle starts from the front corners of the main frame.

# Front of the frame is at y = +frame_length/2
front_y = frame_length / 2
tongue_tip_y = front_y + tongue_length

# Create the left diagonal of the tongue
# Points: (half_width, front_y) to (0, tongue_tip_y)
# We can construct this by lofting or extruding a shape along a path.
# A simpler way with basic primitives is to rotate a box.
import math
angle_rad = math.atan(half_width / tongue_length)
angle_deg = math.degrees(angle_rad)
diagonal_length = math.sqrt(half_width**2 + tongue_length**2)

# Left diagonal beam (connecting left front corner to center tip)
# Position center of beam
left_diag_center_x = -half_width / 2
left_diag_center_y = front_y + tongue_length / 2

left_tongue = (
    cq.Workplane("XY")
    .box(tube_size, diagonal_length, tube_size)
    .rotate((0,0,1), (0,0,0), -angle_deg) # Rotate to match angle
    .translate((left_diag_center_x, left_diag_center_y, 0))
)

# Right diagonal beam
right_diag_center_x = half_width / 2
right_diag_center_y = front_y + tongue_length / 2

right_tongue = (
    cq.Workplane("XY")
    .box(tube_size, diagonal_length, tube_size)
    .rotate((0,0,1), (0,0,0), angle_deg)
    .translate((right_diag_center_x, right_diag_center_y, 0))
)

# 4. Create Tongue Cross-Brace
# It appears in the image there is a small brace inside the triangle.
# Let's put it roughly in the middle of the tongue length.
brace_y_pos = front_y + (tongue_length * 0.4) 
# Calculate width at this Y position using similar triangles
# Width at base = frame_width, width at tip = 0
# Distance from tip = (tongue_tip_y - brace_y_pos)
dist_from_tip = tongue_tip_y - brace_y_pos
# Ratio = dist_from_tip / tongue_length
current_half_width_at_brace = (dist_from_tip / tongue_length) * half_width
brace_length = (current_half_width_at_brace * 2) 

# Adjust length slightly to intersect properly without sticking out too much, 
# though union handles overlap fine.
tongue_brace = (
    cq.Workplane("XY")
    .box(brace_length, tube_size, tube_size)
    .translate((0, brace_y_pos, 0))
)

# Combine all parts
result = (
    left_rail
    .union(right_rail)
    .union(cross_members)
    .union(left_tongue)
    .union(right_tongue)
    .union(tongue_brace)
)