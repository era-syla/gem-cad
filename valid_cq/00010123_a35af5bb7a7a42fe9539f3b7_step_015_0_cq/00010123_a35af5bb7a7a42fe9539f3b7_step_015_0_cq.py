import cadquery as cq
import math

# --- Parameters ---
outer_diameter = 20.0  # Overall diameter of the knurled part
inner_diameter = 8.0   # Diameter of the central hole
height = 60.0          # Height of the cylinder
num_ridges = 60        # Number of ridges for the knurling effect
ridge_depth = 0.5      # How deep the ridges cut in

# --- Helper Logic ---
# Calculate the radius for the base cylinder and the outer peaks
base_radius = (outer_diameter / 2.0) - ridge_depth
outer_radius = outer_diameter / 2.0

# --- Geometry Construction ---

# 1. Create the base profile for the knurled exterior
# We'll create a single "tooth" or ridge and pattern it
angle_step = 360.0 / num_ridges

# Create the profile points for one ridge
# Points: (base_r, 0), (outer_r, half_angle), (base_r, angle)
# We need to convert polar to cartesian for the sketch
p0 = (base_radius, 0)

# Calculate mid point (tip of the ridge)
mid_angle_rad = math.radians(angle_step / 2.0)
p1_x = outer_radius * math.cos(mid_angle_rad)
p1_y = outer_radius * math.sin(mid_angle_rad)
p1 = (p1_x, p1_y)

# Calculate end point of the segment
end_angle_rad = math.radians(angle_step)
p2_x = base_radius * math.cos(end_angle_rad)
p2_y = base_radius * math.sin(end_angle_rad)
p2 = (p2_x, p2_y)

# Construct the sketch for the full cross-section
# We create one segment and polar array it
ridge_sketch = (
    cq.Workplane("XY")
    .polarArray(base_radius, 0, 360, num_ridges)
    .polyline([(0, 0), (p1_x - base_radius, p1_y), (p2_x - base_radius, p2_y)])
    .close()
)

# A more robust way using a custom profile sketch
# Let's generate all points for the profile manually to ensure a closed loop without artifacts
points = []
for i in range(num_ridges):
    theta_start = math.radians(i * angle_step)
    theta_mid = math.radians((i + 0.5) * angle_step)
    
    # Valley point (start of ridge)
    points.append((base_radius * math.cos(theta_start), base_radius * math.sin(theta_start)))
    # Peak point (tip of ridge)
    points.append((outer_radius * math.cos(theta_mid), outer_radius * math.sin(theta_mid)))

# 2. Extrude the knurled profile
result = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(height)
)

# 3. Cut the central hole
result = result.faces(">Z").workplane().circle(inner_diameter / 2.0).cutThruAll()

# 4. Optional: Add small chamfers to the top and bottom edges for realism (looks slightly chamfered in image)
# Selecting outer edges might be computationally expensive due to the many ridges.
# Let's apply a chamfer only to the inner hole for a clean look, or skip if edges are too complex.
# In the image, the top face looks flat, maybe a very slight chamfer on the hole.
try:
    result = result.faces(">Z or <Z").edges(cq.selectors.RadiusNthSelector(0)).chamfer(0.5)
except:
    pass # If selection fails, return unchamfered

# Export or display
# show_object(result)