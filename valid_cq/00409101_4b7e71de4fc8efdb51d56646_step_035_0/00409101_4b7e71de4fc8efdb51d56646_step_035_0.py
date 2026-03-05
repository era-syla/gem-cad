import cadquery as cq

# -- Parameters --
length = 300.0
width = 180.0
thickness = 8.0
flange_width = 30.0
step_depth = 3.0       # Depth of the step down for the flanges
large_hole_dia = 18.0
large_hole_x = 75.0    # Offset from center
small_hole_dia = 3.5
group_spacing = 110.0  # Distance from center to outer hole groups
pair_spacing = 12.0    # Spacing between holes in a pair

# -- Modeling --

# 1. Create the base block
result = cq.Workplane("XY").box(length, width, thickness)

# 2. Create the stepped flanges
# We remove material from the top face along the long edges
# Calculate the Y offset for the cutter rectangles
# The cutter is centered on the flange area
flange_center_y_offset = (width - flange_width) / 2.0

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([
        (0, -flange_center_y_offset),  # Near side flange
        (0, flange_center_y_offset)     # Far side flange
    ])
    .rect(length, flange_width)
    .cutBlind(-step_depth)
)

# 3. Create the Large Hole
# Located in the central raised section, offset to the right
result = (
    result.faces(">Z")  # Select the highest face (central plateau)
    .workplane()
    .moveTo(large_hole_x, 0)
    .hole(large_hole_dia)
)

# 4. Create the Small Mounting Holes
# Located on the near flange (Y < 0). There are 3 groups of pairs.
small_hole_points = []
near_flange_y_center = -(width / 2.0) + (flange_width / 2.0)
x_locations = [-group_spacing, 0, group_spacing]

for x in x_locations:
    # Pair of holes aligned perpendicular to the edge
    small_hole_points.append((x, near_flange_y_center - pair_spacing/2))
    small_hole_points.append((x, near_flange_y_center + pair_spacing/2))

result = (
    result.faces(">Z")  # Sketch on the top plane
    .workplane()
    .pushPoints(small_hole_points)
    .hole(small_hole_dia)  # Project hole cut downwards through the part
)