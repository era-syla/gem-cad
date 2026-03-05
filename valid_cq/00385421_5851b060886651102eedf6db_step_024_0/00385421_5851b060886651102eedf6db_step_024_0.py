import cadquery as cq
import math

# --- Parametric Dimensions ---
shaft_diameter = 3.0
shaft_length = 60.0

gear_outer_diameter = 14.0
gear_thickness = 6.0
num_teeth = 22

# --- Derived Gear Parameters ---
# Calculate module based on Outer Diameter and Tooth Count (OD = m * (N + 2))
module = gear_outer_diameter / (num_teeth + 2)
# Calculate Root Diameter (Approximate standard clearance: OD - 2.25 * m - 2 * m is pitch)
# Actually Total Depth approx 2.25 * m
# Root Diameter = Outer Diameter - 2 * (2.25 * m) is wrong, depth is radial.
# Root Diameter = Outer Diameter - 2 * (2.25 * m) is roughly correct for full depth.
root_diameter = gear_outer_diameter - (4.5 * module)
# Ensure root is larger than shaft
if root_diameter < shaft_diameter + 1.0:
    root_diameter = shaft_diameter + 1.0

r_root = root_diameter / 2.0
r_outer = gear_outer_diameter / 2.0

# --- Geometry Generation ---

# 1. Create the Shaft
# A cylinder centered at the origin, aligned with Z-axis
shaft = (cq.Workplane("XY")
         .circle(shaft_diameter / 2.0)
         .extrude(shaft_length / 2.0, both=True))

# 2. Generate Gear Profile Points
# We calculate the vertices for a simplified trapezoidal gear profile
points = []
angle_step = 2 * math.pi / num_teeth  # Angular pitch per tooth

# Angular widths for the tooth shape
# Tooth root width ~ 50% of pitch
# Tooth tip width ~ 25% of pitch (tapered profile)
half_root_angle = (angle_step * 0.50) / 2.0
half_tip_angle = (angle_step * 0.25) / 2.0

for i in range(num_teeth):
    center_angle = i * angle_step
    
    # Calculate 4 points for each tooth
    # P1: Root start (left side of tooth base)
    theta1 = center_angle - half_root_angle
    p1 = (r_root * math.cos(theta1), r_root * math.sin(theta1))
    
    # P2: Tip start (left side of tooth tip)
    theta2 = center_angle - half_tip_angle
    p2 = (r_outer * math.cos(theta2), r_outer * math.sin(theta2))
    
    # P3: Tip end (right side of tooth tip)
    theta3 = center_angle + half_tip_angle
    p3 = (r_outer * math.cos(theta3), r_outer * math.sin(theta3))
    
    # P4: Root end (right side of tooth base)
    theta4 = center_angle + half_root_angle
    p4 = (r_root * math.cos(theta4), r_root * math.sin(theta4))
    
    points.extend([p1, p2, p3, p4])

# 3. Create the Gear Solid
# Draw the profile defined by points, close it, and extrude
gear = (cq.Workplane("XY")
        .polyline(points)
        .close()
        .extrude(gear_thickness / 2.0, both=True))

# 4. Combine Shaft and Gear
result = shaft.union(gear)