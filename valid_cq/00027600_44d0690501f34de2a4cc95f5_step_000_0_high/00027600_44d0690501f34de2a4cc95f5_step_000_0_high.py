import cadquery as cq
import math

# -----------------------------------------------------------------------------
# Parameters
# -----------------------------------------------------------------------------
# Gear Geometry
num_teeth = 40
module = 2.0
thickness = 15.0
pressure_angle_deg = 20.0

# Hub/Mounting Geometry
bore_diameter = 25.0
bolt_circle_diameter = 55.0
num_mounting_holes = 5
mounting_hole_diameter = 8.0

# -----------------------------------------------------------------------------
# Calculations
# -----------------------------------------------------------------------------
pitch_radius = (module * num_teeth) / 2.0
outer_radius = pitch_radius + module
root_radius = pitch_radius - (1.25 * module)

# -----------------------------------------------------------------------------
# Profile Generation
# -----------------------------------------------------------------------------
# We generate the gear profile as a list of vertices for a polyline.
# This creates a trapezoidal approximation of an involute tooth which is 
# robust and visually accurate for this purpose.

points = []
angle_step = (2 * math.pi) / num_teeth
half_tooth_angle = angle_step / 4.0 

# Define width factors to approximate the involute shape
# Base is wider, tip is narrower
theta_base = half_tooth_angle * 1.2 
theta_tip = half_tooth_angle * 0.6

for i in range(num_teeth):
    center_angle = i * angle_step
    
    # Calculate vertex angles
    a_root_left = center_angle - theta_base
    a_tip_left = center_angle - theta_tip
    a_tip_right = center_angle + theta_tip
    a_root_right = center_angle + theta_base
    
    # Generate coordinates
    p1 = (root_radius * math.cos(a_root_left), root_radius * math.sin(a_root_left))
    p2 = (outer_radius * math.cos(a_tip_left), outer_radius * math.sin(a_tip_left))
    p3 = (outer_radius * math.cos(a_tip_right), outer_radius * math.sin(a_tip_right))
    p4 = (root_radius * math.cos(a_root_right), root_radius * math.sin(a_root_right))
    
    points.extend([p1, p2, p3, p4])

# -----------------------------------------------------------------------------
# Solid Modeling
# -----------------------------------------------------------------------------

# 1. Create the main gear body by extruding the profile
result = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(thickness)
)

# 2. Cut the central bore
result = (
    result.faces(">Z")
    .workplane()
    .circle(bore_diameter / 2.0)
    .cutBlind(-thickness)
)

# 3. Cut the mounting holes pattern
result = (
    result.faces(">Z")
    .workplane()
    .polarArray(bolt_circle_diameter / 2.0, 0, 360, num_mounting_holes)
    .circle(mounting_hole_diameter / 2.0)
    .cutBlind(-thickness)
)