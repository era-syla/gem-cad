import cadquery as cq
import math

# --- Parameters ---
num_teeth = 10
outside_dia = 100.0  # Tip diameter
root_dia = 70.0      # Root diameter
thickness = 15.0     # Gear thickness
bore_dia = 12.0      # Central hole diameter

# --- Derived Dimensions ---
outside_radius = outside_dia / 2.0
root_radius = root_dia / 2.0
pitch_angle = 360.0 / num_teeth

# Angular half-widths for the tooth profile (relative to tooth centerline)
# Adjust these factors to change the "chunkiness" of the teeth
angle_root = (pitch_angle / 4.0) * 1.15  # Wider at root
angle_tip = (pitch_angle / 4.0) * 0.5    # Narrower at tip

# --- Helper Function ---
def polar_to_cartesian(r, angle_deg):
    """Converts polar coordinates (radius, degrees) to (x, y)."""
    rad = math.radians(angle_deg)
    return (r * math.cos(rad), r * math.sin(rad))

# --- Geometry Construction ---

# 1. Create the Central Hub (Root Cylinder)
# We create a cylinder representing the gear body up to the root radius.
# We add a small tolerance to the radius for the tooth union overlap, 
# but effectively the hub is the root circle.
hub = cq.Workplane("XY").circle(root_radius).extrude(thickness)

# 2. Define Single Tooth Geometry
# We calculate key points for one tooth profile centered on the X-axis.
# Points are calculated for the top half (positive Y) and mirrored logic for bottom half.

# Start slightly inside the root radius to ensuring a clean boolean union overlap
r_base_overlap = root_radius - 0.5 

# Coordinate calculations
p_root_neg = polar_to_cartesian(r_base_overlap, -angle_root)
p_root_pos = polar_to_cartesian(r_base_overlap, angle_root)
p_tip_neg = polar_to_cartesian(outside_radius, -angle_tip)
p_tip_pos = polar_to_cartesian(outside_radius, angle_tip)

# Control points for the convex involute-like flank
# Positioned at mid-radius with a slightly wider angle to create the outward curve
mid_radius = (root_radius + outside_radius) / 2.0
mid_angle = (angle_root + angle_tip) / 2.0 * 1.2
p_mid_neg = polar_to_cartesian(mid_radius, -mid_angle)
p_mid_pos = polar_to_cartesian(mid_radius, mid_angle)

# Create the solid for a single tooth
tooth = (
    cq.Workplane("XY")
    .moveTo(*p_root_neg)                 # Start at bottom root
    .threePointArc(p_mid_neg, p_tip_neg) # Curve up to bottom tip
    .lineTo(*p_tip_pos)                  # Flat top of tooth
    .threePointArc(p_mid_pos, p_root_pos)# Curve down to top root
    .close()
    .extrude(thickness)
)

# 3. Pattern and Union Teeth
# Start with the hub and union each rotated tooth instance
result = hub
for i in range(num_teeth):
    angle = i * pitch_angle
    # Rotate the tooth solid around the Z-axis (0,0,1) at origin (0,0,0)
    rotated_tooth = tooth.rotate((0, 0, 0), (0, 0, 1), angle)
    result = result.union(rotated_tooth)

# 4. Create the Bore
# Cut the central hole through the entire gear
result = result.faces(">Z").workplane().hole(bore_dia)