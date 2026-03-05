import cadquery as cq

# --- Parametric Dimensions ---
# Overall dimensions of the plate
length = 200.0  # Total length of the plate
width = 40.0    # Width of the plate
thickness = 5.0 # Thickness of the plate

# Central hole dimensions
center_hole_diameter = 10.0
# Optional: Counterbore depth if desired, though image looks like a simple through hole or slightly chamfered.
# We will stick to a clean through-hole as the primary feature.

# Mounting hole dimensions (small holes at ends)
small_hole_diameter = 3.0

# Pattern parameters for small holes
# Looking at the image, there are 4 holes on each end.
# They seem arranged in a rectangular pattern near the edges.
end_hole_spacing_x = 20.0 # Distance between holes along length at one end
end_hole_spacing_y = 25.0 # Distance between holes along width
end_offset_x = 25.0       # Distance from the center of the plate to the center of the hole group

# Calculated positions for the small holes
# We need two groups of 4 holes.
# Group 1 (Left): Center is roughly at x = -(length/2 - margin)
# Group 2 (Right): Center is roughly at x = +(length/2 - margin)
# Let's define the centers of the 4-hole clusters relative to the main center.
cluster_offset = (length / 2) - (end_hole_spacing_x / 2) - 10.0 # 10mm margin from edge

# --- Modeling Process ---

# 1. Create the base rectangular plate
result = cq.Workplane("XY").box(length, width, thickness)

# 2. Create the central large hole
result = result.faces(">Z").workplane().hole(center_hole_diameter)

# 3. Create the small mounting holes
# We will create a list of points for all 8 small holes.
hole_points = []

# Define the relative offsets for a single 4-hole cluster
x_offsets = [-end_hole_spacing_x / 2, end_hole_spacing_x / 2]
y_offsets = [-end_hole_spacing_y / 2, end_hole_spacing_y / 2]

# Cluster centers (Left and Right sides)
cluster_centers = [-cluster_offset, cluster_offset]

for cluster_x in cluster_centers:
    for dx in x_offsets:
        for dy in y_offsets:
            hole_points.append((cluster_x + dx, dy))

# Cut the small holes at the defined points
result = result.faces(">Z").workplane().pushPoints(hole_points).hole(small_hole_diameter)

# Return the final result
if __name__ == "__main__":
    # If running in an environment that supports show_object (like CQ-Editor), display it
    try:
        show_object(result)
    except NameError:
        pass