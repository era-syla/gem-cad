import cadquery as cq

# --- Model Parameters ---
total_height = 400.0     # Total length of the shaft
shaft_radius = 3.5       # Radius of the main rod
node_radius = 5.5        # Radius of the protruding rings/nodes
node_height = 4.0        # Height of each ring/node
num_nodes = 11           # Total number of rings
bottom_offset = 30.0     # Distance from bottom to center of first ring
top_offset = 15.0        # Distance from top to center of last ring

# --- Calculation ---
# Calculate the vertical spacing (pitch) between nodes
# Distribution span is the distance between the first and last node centers
distribution_span = total_height - bottom_offset - top_offset
if num_nodes > 1:
    spacing = distribution_span / (num_nodes - 1)
else:
    spacing = 0

# --- Geometry Construction ---
# We construct the object by defining a 2D profile on the XZ plane
# and revolving it around the Z-axis. This creates a single valid solid.

# List of points (r, z) for the profile
points = []
points.append((0, 0))                  # Start at origin
points.append((shaft_radius, 0))       # Bottom edge of shaft

# Iterate to generate the profile segments for each node
for i in range(num_nodes):
    z_center = bottom_offset + i * spacing
    z_bot = z_center - node_height / 2.0
    z_top = z_center + node_height / 2.0
    
    # Add profile points:
    # 1. Vertical line on shaft up to the node bottom
    points.append((shaft_radius, z_bot))
    # 2. Horizontal line out to node radius
    points.append((node_radius, z_bot))
    # 3. Vertical line up the node face
    points.append((node_radius, z_top))
    # 4. Horizontal line back to shaft radius
    points.append((shaft_radius, z_top))

# Complete the profile to the top of the shaft
points.append((shaft_radius, total_height))
points.append((0, total_height))       # Close back to the axis

# Create the solid
result = (
    cq.Workplane("XZ")
    .polyline(points)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0)) # Revolve around the Z-axis (local Y of XZ plane)
)