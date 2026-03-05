import cadquery as cq
import math

# Drone frame / X-shaped plate
# Overall dimensions estimated from image

thickness = 3
arm_width = 18
arm_length = 80
center_size = 50
pad_radius = 20
pad_thickness = thickness

# Create the center body
center = (
    cq.Workplane("XY")
    .rect(center_size, center_size)
    .extrude(thickness)
)

# Arm directions: front-right, front-left, back-right, back-left (X configuration)
arm_angle_offsets = [45, 135, 225, 315]

def make_arm(angle_deg):
    """Create an arm pointing in the given direction"""
    angle_rad = math.radians(angle_deg)
    
    # Arm goes from center outward
    half_w = arm_width / 2
    total_length = arm_length + center_size / 2 * math.sqrt(2) / 2
    
    arm = (
        cq.Workplane("XY")
        .rect(arm_width, arm_length)
        .extrude(thickness)
        .translate((0, arm_length / 2, 0))
    )
    
    # Rotate to angle
    arm = arm.rotate((0, 0, 0), (0, 0, 1), angle_deg - 90)
    
    return arm

def make_pad(angle_deg):
    """Create a rounded pad at the end of an arm"""
    angle_rad = math.radians(angle_deg)
    
    # Position at end of arm
    dist = arm_length + center_size * 0.3
    x = dist * math.cos(angle_rad)
    y = dist * math.sin(angle_rad)
    
    pad = (
        cq.Workplane("XY")
        .circle(pad_radius)
        .extrude(thickness)
        .translate((x, y, 0))
    )
    
    return pad

# Start with center
result = center

# Add arms and pads
for angle in arm_angle_offsets:
    angle_rad = math.radians(angle)
    
    # Arm center position
    arm_center_dist = center_size * 0.3 + arm_length / 2
    arm_cx = arm_center_dist * math.cos(angle_rad)
    arm_cy = arm_center_dist * math.sin(angle_rad)
    
    # Create arm as a box
    arm = (
        cq.Workplane("XY")
        .rect(arm_width, arm_length)
        .extrude(thickness)
        .translate((arm_cx, arm_cy, 0))
        .rotate((0, 0, 0), (0, 0, 1), angle)
    )
    
    result = result.union(arm)
    
    # Pad at the end
    pad_dist = center_size * 0.3 + arm_length
    pad_x = pad_dist * math.cos(angle_rad)
    pad_y = pad_dist * math.sin(angle_rad)
    
    pad = (
        cq.Workplane("XY")
        .circle(pad_radius)
        .extrude(thickness)
        .translate((pad_x, pad_y, 0))
    )
    
    result = result.union(pad)

# Add mounting holes in the pads (2 holes per pad)
for angle in arm_angle_offsets:
    angle_rad = math.radians(angle)
    pad_dist = center_size * 0.3 + arm_length
    pad_x = pad_dist * math.cos(angle_rad)
    pad_y = pad_dist * math.sin(angle_rad)
    
    # Perpendicular direction for hole offset
    perp_x = -math.sin(angle_rad)
    perp_y = math.cos(angle_rad)
    
    hole_offset = 8
    for sign in [-1, 1]:
        hx = pad_x + sign * perp_x * hole_offset
        hy = pad_y + sign * perp_y * hole_offset
        
        result = (
            result
            .faces(">Z")
            .workplane()
            .pushPoints([(hx, hy)])
            .circle(1.5)
            .cutThruAll()
        )

# Add center holes
center_hole_positions = [(10, 10), (-10, 10), (10, -10), (-10, -10)]
for hx, hy in center_hole_positions:
    result = (
        result
        .faces(">Z")
        .workplane()
        .pushPoints([(hx, hy)])
        .circle(2)
        .cutThruAll()
    )