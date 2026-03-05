import cadquery as cq
import math

# --- Parameters ---
# Overall dimensions of the friction plate / splined ring
outer_diameter = 120.0
thickness = 2.0

# Internal Spline Parameters
num_teeth = 42
inner_tip_diameter = 95.0   # Diameter at the innermost tip of the teeth
inner_root_diameter = 102.0 # Diameter at the root of the teeth (gap bottom)

# Tooth profile shape ratios (fractions of the angular pitch)
# Adjust these to change the shape of the teeth (trapezoidal profile)
ratio_tip = 0.12    # Angular fraction for the flat tip of the tooth
ratio_root = 0.18   # Angular fraction for the flat bottom of the gap
# The remaining angle is divided between the two slopes
ratio_slope = (1.0 - ratio_tip - ratio_root) / 2.0

# --- Geometry Generation ---

# List to store the vertices of the inner profile
inner_profile_points = []
angle_step = 360.0 / num_teeth

# Helper function: Polar to Cartesian coordinates
def polar_to_cartesian(r, angle_deg):
    rad = math.radians(angle_deg)
    return (r * math.cos(rad), r * math.sin(rad))

# Generate points for the inner splined wire
for i in range(num_teeth):
    start_angle = i * angle_step
    
    # Calculate absolute angles for the four corners of a trapezoidal tooth/gap cycle
    # Sequence: Tip Start -> Tip End -> Slope Down -> Root Start -> Root End -> Slope Up
    a1 = start_angle
    a2 = start_angle + (angle_step * ratio_tip)
    a3 = start_angle + (angle_step * (ratio_tip + ratio_slope))
    a4 = start_angle + (angle_step * (ratio_tip + ratio_slope + ratio_root))
    
    r_tip = inner_tip_diameter / 2.0
    r_root = inner_root_diameter / 2.0
    
    # Append the four points defining one segment of the spline
    inner_profile_points.append(polar_to_cartesian(r_tip, a1))   # Start of tooth tip
    inner_profile_points.append(polar_to_cartesian(r_tip, a2))   # End of tooth tip
    inner_profile_points.append(polar_to_cartesian(r_root, a3))  # Start of gap root
    inner_profile_points.append(polar_to_cartesian(r_root, a4))  # End of gap root

# Create the solid model
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)      # Create the outer circular boundary
    .polyline(inner_profile_points)    # Create the inner splined boundary
    .close()                           # Close the inner wire profile
    .extrude(thickness)                # Extrude the enclosed area
)