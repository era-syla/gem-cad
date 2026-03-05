import cadquery as cq

# Parameters for Part 1 (Large L-shaped block)
p1_height = 60.0
p1_width = 40.0
p1_depth = 50.0
p1_top_flat = 25.0     # Depth of the top flat surface
p1_cutout_width = 20.0
p1_cutout_depth = 35.0 # Depth of the cutout from the front

# Parameters for Part 2 (Small separate block)
p2_height = 30.0
p2_width = 15.0
p2_depth = 30.0
# Calculate top flat depth to maintain similar slope angle to Part 1
# Slope run = (p1_depth - p1_top_flat) for height p1_height
slope_ratio = p1_height / (p1_depth - p1_top_flat)
p2_slope_run = p2_height / slope_ratio
p2_top_flat = p2_depth - p2_slope_run

# --- Construction of Part 1 ---

# Define the side profile (YZ plane)
# Origin (0,0) corresponds to the bounding box front-bottom corner
pts1 = [
    (0, 0),                   # Bottom Front (start of slope)
    (p1_depth, 0),            # Bottom Back
    (p1_depth, p1_height),    # Top Back
    (p1_depth - p1_top_flat, p1_height) # Top Front edge
]

# Create the base prism
part1_base = (
    cq.Workplane("YZ")
    .polyline(pts1)
    .close()
    .extrude(p1_width)
)

# Create the cutout geometry (rectangular block)
# Removing material from the Front-Left corner
cutout_solid = (
    cq.Workplane("XY")
    .box(p1_cutout_width, p1_cutout_depth, p1_height, centered=False)
)

# Apply the cut
part1 = part1_base.cut(cutout_solid)


# --- Construction of Part 2 ---

# Define the side profile for the smaller block
pts2 = [
    (0, 0),
    (p2_depth, 0),
    (p2_depth, p2_height),
    (p2_depth - p2_top_flat, p2_height)
]

part2_base = (
    cq.Workplane("YZ")
    .polyline(pts2)
    .close()
    .extrude(p2_width)
)

# Position Part 2 relative to Part 1
# Place it to the left (negative X) and slightly forward (negative Y)
gap_x = 10.0
gap_y = 10.0
part2 = part2_base.translate((-p2_width - gap_x, -gap_y, 0))


# --- Final Result ---
result = part1.union(part2)