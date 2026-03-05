import cadquery as cq
import math

# -----------------------------------------------------------------------------
# Parametric Definitions
# -----------------------------------------------------------------------------

# Main Plate Dimensions
plate_width = 500.0   # X-axis dimension
plate_depth = 400.0   # Y-axis dimension
plate_thick = 4.0     # Z-axis dimension
chamfer_dim = 40.0    # Size of the corner chamfers

# Fan Cutout Parameters
fan_dia_outer = 90.0
fan_bar_width = 8.0
fan_hole_spacing = 82.0
fan_mount_hole_dia = 4.5
fan_pos_x = -150.0       # X position for fans (Left side)
fan_spacing_y = 110.0    # Distance between the two fans

# Rectangular Switch/Port Cutout
rect_cut_w = 30.0
rect_cut_h = 20.0
rect_pos_x = -120.0
rect_pos_y = 130.0       # Located behind the rear fan

# Center Slot Parameters
slot_length = 50.0
slot_width = 10.0
slot_angle = 0.0

# Right Side Large Hole
large_hole_dia = 55.0
large_hole_pos_x = 150.0
large_hole_pos_y = -80.0 # Located towards the front right

# Mounting Hole Parameters
mnt_hole_dia = 3.5

# -----------------------------------------------------------------------------
# Geometry Construction
# -----------------------------------------------------------------------------

# 1. Base Plate
# Create a rectangular plate centered at origin
# Chamfer only the front two corners (assumed to be at -Y)
result = (
    cq.Workplane("XY")
    .box(plate_width, plate_depth, plate_thick)
    .edges("|Z and <Y")  # Select vertical edges at the front (min Y)
    .chamfer(chamfer_dim)
)

# 2. Fan Grills (Left Side)
# Create a sketch for the fan grill: Circle minus a cross
grill_sketch = (
    cq.Sketch()
    .circle(fan_dia_outer / 2)
    .rect(fan_dia_outer + 5, fan_bar_width, mode='s')  # Subtract horizontal bar
    .rect(fan_bar_width, fan_dia_outer + 5, mode='s')  # Subtract vertical bar
)

# Define locations for the two fans
fan_locations = [
    (fan_pos_x, -fan_spacing_y / 2),
    (fan_pos_x, fan_spacing_y / 2)
]

for fx, fy in fan_locations:
    # Cut the grill pattern
    result = (
        result.workplane()
        .center(fx, fy)
        .placeSketch(grill_sketch)
        .cutThruAll()
    )
    
    # Cut the 4 mounting holes for the fan
    result = (
        result.workplane()
        .center(fx, fy)
        .rect(fan_hole_spacing, fan_hole_spacing, forConstruction=True)
        .vertices()
        .circle(fan_mount_hole_dia / 2)
        .cutThruAll()
    )

# 3. Rectangular Cutout (Top Left)
result = (
    result.workplane()
    .center(rect_pos_x, rect_pos_y)
    .rect(rect_cut_w, rect_cut_h)
    .cutThruAll()
)

# 4. Center Slot
result = (
    result.workplane()
    .center(0, 0)
    .slot2D(slot_length, slot_width, angle=slot_angle)
    .cutThruAll()
)

# 5. Large Hole (Bottom Right)
result = (
    result.workplane()
    .center(large_hole_pos_x, large_hole_pos_y)
    .circle(large_hole_dia / 2)
    .cutThruAll()
)

# 6. General Mounting Holes
# Generate a list of points for various mounting holes
hole_points = []

# Perimeter holes along top and bottom edges (excluding chamfer areas)
for x in [-180, -60, 60, 180]:
    hole_points.append((x, plate_depth/2 - 15))   # Back edge
    if abs(x) < 150: # Avoid chamfer area on front
        hole_points.append((x, -plate_depth/2 + 15))  # Front edge

# Holes near the chamfered edges
hole_points.append((plate_width/2 - chamfer_dim + 10, -plate_depth/2 + 30))
hole_points.append((-plate_width/2 + chamfer_dim - 10, -plate_depth/2 + 30))

# Cluster of holes around the large right hole
radius_cluster = large_hole_dia/2 + 12
for angle in range(0, 360, 45):
    rad = math.radians(angle)
    hx = large_hole_pos_x + radius_cluster * math.cos(rad)
    hy = large_hole_pos_y + radius_cluster * math.sin(rad)
    hole_points.append((hx, hy))

# Additional mounting points near sides
hole_points.append((plate_width/2 - 15, 0))
hole_points.append((plate_width/2 - 15, 100))
hole_points.append((-plate_width/2 + 15, 0))

# Execute cut for all collected hole points
result = (
    result.workplane()
    .pushPoints(hole_points)
    .circle(mnt_hole_dia / 2)
    .cutThruAll()
)