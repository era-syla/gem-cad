import cadquery as cq
import math

# --- Parameters ---
thickness = 10.0        # Thickness of the plate
leg_length = 100.0      # Length of the V legs along the outer edge
leg_width = 25.0        # Width of the legs
angle_deg = 35.0        # Half-angle of the V (degrees)
notch_width = 12.0      # Width of the rectangular cutout at the tip
notch_depth = 15.0      # Depth of the rectangular cutout at the tip

# --- Helper Calculations ---
angle_rad = math.radians(angle_deg)

# Define vertices for the top half of the V shape (assuming X-axis symmetry)
# Origin (0,0) is the theoretical sharp tip of the V
p0 = (0, 0)

# P1: Outer end of the leg
p1_x = leg_length * math.cos(angle_rad)
p1_y = leg_length * math.sin(angle_rad)
p1 = (p1_x, p1_y)

# P2: Inner end of the leg
# Calculated to ensure the end face is perpendicular to the leg's length
# We move 'leg_width' distance perpendicular to the leg vector
p2_x = p1_x + leg_width * math.sin(angle_rad)
p2_y = p1_y - leg_width * math.cos(angle_rad)
p2 = (p2_x, p2_y)

# P3: Inner crotch point
# Intersection of the inner leg edge with the X-axis (axis of symmetry)
# Geometrically, this is at x = leg_width / sin(angle)
p3_x = leg_width / math.sin(angle_rad)
p3 = (p3_x, 0)

# --- Model Construction ---

# 1. Create the top half of the V
top_half = (
    cq.Workplane("XY")
    .polyline([p0, p1, p2, p3])
    .close()
    .extrude(thickness)
)

# 2. Mirror to create the bottom half and union them
# Mirroring about the XZ plane creates the symmetry along the X-axis
bottom_half = top_half.mirror(mirrorPlane="XZ")
base_v = top_half.union(bottom_half)

# 3. Create the notch cutout
# We create a rectangular solid at the origin to remove material
notch_cutout = (
    cq.Workplane("XY")
    .center(notch_depth / 2.0, 0)  # Center the rectangle so it starts at x=0
    .rect(notch_depth, notch_width)
    .extrude(thickness)
)

# 4. Final Operation
result = base_v.cut(notch_cutout)