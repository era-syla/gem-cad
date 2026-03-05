import cadquery as cq
from math import cos, sin, tan, pi, radians, acos

def involute_angle(radius, base_radius):
    """
    Calculate the involute angle (theta) for a given radius.
    theta = tan(alpha) - alpha, where cos(alpha) = base_radius / radius
    """
    if radius <= base_radius:
        return 0.0
    alpha = acos(base_radius / radius)
    return tan(alpha) - alpha

def generate_gear_profile_points(module, num_teeth, pressure_angle=20.0):
    """
    Generates the list of (x, y) coordinates for a complete involute gear profile.
    """
    # Gear Dimensions
    pitch_diameter = module * num_teeth
    pitch_radius = pitch_diameter / 2.0
    base_radius = pitch_radius * cos(radians(pressure_angle))
    addendum = module
    dedendum = 1.2 * module
    outer_radius = pitch_radius + addendum
    root_radius = pitch_radius - dedendum
    
    # Tooth Calculation Parameters
    # Angle at pitch circle for involute
    theta_pitch = involute_angle(pitch_radius, base_radius)
    # Angular half-thickness of tooth at pitch circle
    # Total pitch angle = 2*pi/N. Tooth thickness is half of that.
    half_tooth_angle = pi / (2 * num_teeth)
    
    # Angle offset to center the tooth on the X-axis
    # The involute equation defines theta=0 at the base circle start. 
    # We need to shift it so the tooth thickness is correct at the pitch circle.
    angle_offset = theta_pitch + half_tooth_angle
    
    # Generate points for one tooth
    # Resolution of the involute curve
    steps = 7
    
    # Determine start radius for involute (cannot be below base circle)
    r_start = max(base_radius, root_radius)
    
    right_flank = []
    left_flank = []
    
    # 1. Generate Involute Flanks
    for i in range(steps + 1):
        r = r_start + (outer_radius - r_start) * (i / steps)
        theta = involute_angle(r, base_radius)
        
        # Right flank (negative angle side)
        angle_r = -angle_offset + theta
        right_flank.append((r * cos(angle_r), r * sin(angle_r)))
        
        # Left flank (positive angle side)
        angle_l = angle_offset - theta
        left_flank.append((r * cos(angle_l), r * sin(angle_l)))
        
    # 2. Handle Root Undercut (Straight radial lines if root < base)
    if root_radius < base_radius:
        # Add point at root radius maintaining the base angle
        base_angle_r = -angle_offset # theta is 0 at base
        right_flank.insert(0, (root_radius * cos(base_angle_r), root_radius * sin(base_angle_r)))
        
        base_angle_l = angle_offset
        left_flank.append((root_radius * cos(base_angle_l), root_radius * sin(base_angle_l)))
        
    # Reverse left flank to go from Tip -> Root
    left_flank.reverse()
    
    # Combine into single tooth points: Root(R) -> Tip(R) -> Tip(L) -> Root(L)
    one_tooth = right_flank + left_flank
    
    # 3. Pattern around the circle
    all_points = []
    angular_pitch = 2 * pi / num_teeth
    
    for i in range(num_teeth):
        angle = i * angular_pitch
        c = cos(angle)
        s = sin(angle)
        
        # Rotate all points of the tooth
        for x, y in one_tooth:
            rx = x * c - y * s
            ry = x * s + y * c
            all_points.append((rx, ry))
            
    return all_points, root_radius

def create_gear_object(module, num_teeth, gear_thick, hub_thick):
    # Generate 2D profile
    points, root_radius = generate_gear_profile_points(module, num_teeth)
    
    # Create Gear solid (Extruded Z+)
    gear_body = (
        cq.Workplane("XY")
        .polyline(points)
        .close()
        .extrude(gear_thick)
    )
    
    # Create Hub solid (Cylinder on back, Extruded Z-)
    # Radius matches root radius for smooth transition
    hub_body = (
        cq.Workplane("XY")
        .workplane(offset=0.1) # Slight overlap for robust union
        .circle(root_radius)
        .extrude(-(hub_thick + 0.1))
    )
    
    return gear_body.union(hub_body)

# --- Main Parameters ---
module_size = 1.0
gear_thickness = 5.0
hub_thickness = 4.0

# 1. Small Gear (Top-Left)
# Estimated ~20-22 teeth
small_gear_teeth = 22
small_gear = create_gear_object(module_size, small_gear_teeth, gear_thickness, hub_thickness)
# Position: Move back and up-left
small_gear = small_gear.translate((-25, 30, 0))

# 2. Large Gear (Bottom-Right)
# Estimated ~44-48 teeth
large_gear_teeth = 46
large_gear = create_gear_object(module_size, large_gear_teeth, gear_thickness, hub_thickness)
# Position: Move forward and down-right
large_gear = large_gear.translate((25, -30, 0))

# Combine into final result
result = small_gear.union(large_gear)