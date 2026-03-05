import cadquery as cq

# Parameters
disk_diameter = 100.0
disk_thickness = 5.0
center_hole_diameter = 10.0
small_hole_diameter = 3.0
grid_pitch = 12.0  # Spacing between holes in the grid
edge_margin = 3.0  # Minimum distance from hole edge to disk edge

# Calculate grid range
# We need enough points to cover the disk
num_points = int(disk_diameter / grid_pitch) + 2
range_start = -(num_points // 2) * grid_pitch
range_end = (num_points // 2) * grid_pitch + 1

# Generate grid points
hole_locations = []
for x in range(int(range_start), int(range_end), int(grid_pitch)):
    for y in range(int(range_start), int(range_end), int(grid_pitch)):
        # Calculate distance from center to the center of the potential hole
        dist_sq = x*x + y*y
        dist = dist_sq**0.5
        
        # Check if the hole is within the disk (considering margin)
        # And ensure it's not overlapping with the center hole
        max_dist = (disk_diameter / 2.0) - (small_hole_diameter / 2.0) - edge_margin
        min_dist = (center_hole_diameter / 2.0) + (small_hole_diameter / 2.0) + 1.0
        
        if min_dist < dist < max_dist:
            hole_locations.append((x, y))

# Create the base disk
result = (
    cq.Workplane("XY")
    .circle(disk_diameter / 2.0)
    .extrude(disk_thickness)
)

# Cut the center hole
result = (
    result
    .faces(">Z")
    .workplane()
    .hole(center_hole_diameter)
)

# Cut the grid of small holes
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(hole_locations)
    .hole(small_hole_diameter)
)