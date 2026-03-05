import cadquery as cq
import math

# Gear parameters
num_teeth = 10
module = 1.5
pressure_angle = 20  # degrees

# Derived gear parameters
pitch_radius = module * num_teeth / 2
addendum = module
dedendum = 1.25 * module
base_radius = pitch_radius * math.cos(math.radians(pressure_angle))
tip_radius = pitch_radius + addendum
root_radius = pitch_radius - dedendum

# Gear height and hub parameters
gear_height = 20
hub_height = 15
hub_radius = tip_radius * 0.85
bore_radius = 3.0

def involute_point(base_r, t):
    x = base_r * (math.cos(t) + t * math.sin(t))
    y = base_r * (math.sin(t) - t * math.cos(t))
    return (x, y)

def generate_tooth_profile(num_teeth, pitch_r, base_r, tip_r, root_r):
    tooth_angle = 2 * math.pi / num_teeth
    half_tooth_angle = tooth_angle / 2
    
    # Generate involute from base to tip
    t_tip = math.sqrt((tip_r / base_r) ** 2 - 1)
    
    # Involute points from root circle to tip
    t_start = 0
    if root_r > base_r:
        t_start = math.sqrt((root_r / base_r) ** 2 - 1)
    
    n_pts = 10
    inv_pts = []
    for i in range(n_pts + 1):
        t = t_start + (t_tip - t_start) * i / n_pts
        p = involute_point(base_r, t)
        inv_pts.append(p)
    
    # Angle of involute at pitch radius
    t_pitch = math.sqrt((pitch_r / base_r) ** 2 - 1)
    pitch_pt = involute_point(base_r, t_pitch)
    pitch_angle = math.atan2(pitch_pt[1], pitch_pt[0])
    
    # We want the pitch point to be at half_tooth_angle / 2
    target_angle = half_tooth_angle / 2
    rotation = target_angle - pitch_angle
    
    def rotate_pt(pt, angle):
        x, y = pt
        c, s = math.cos(angle), math.sin(angle)
        return (x * c - y * s, x * s + y * c)
    
    # Right flank involute
    right_flank = [rotate_pt(p, rotation) for p in inv_pts]
    
    # Left flank - mirror of right flank
    left_flank = [(x, -y) for x, y in right_flank]
    left_flank = left_flank[::-1]
    
    return right_flank, left_flank, rotation

def build_gear_profile(num_teeth, pitch_r, base_r, tip_r, root_r):
    tooth_angle = 2 * math.pi / num_teeth
    
    right_flank, left_flank, rotation = generate_tooth_profile(
        num_teeth, pitch_r, base_r, tip_r, root_r)
    
    all_points = []
    
    for i in range(num_teeth):
        angle = i * tooth_angle
        
        def rot(pt, a):
            x, y = pt
            c, s = math.cos(a), math.sin(a)
            return (x * c - y * s, x * s + y * c)
        
        # Root point before tooth (on root circle)
        root_angle_start = angle - tooth_angle / 2 + rotation + math.atan2(right_flank[0][1], right_flank[0][0])
        # Actually build from left flank end to right flank start via root arc
        
        # Left flank of current tooth
        for pt in left_flank:
            all_points.append(rot(pt, angle))
        
        # Root arc to next tooth's right flank
        root_end_angle = math.atan2(left_flank[0][1], left_flank[0][0]) + angle
        next_start_angle = math.atan2(right_flank[0][1], right_flank[0][0]) + angle + tooth_angle
        
        # Add a root point
        mid_angle = (root_end_angle + next_start_angle) / 2
        all_points.append((root_r * math.cos(mid_angle), root_r * math.sin(mid_angle)))
        
        # Right flank of next tooth
        for pt in right_flank:
            all_points.append(rot(pt, angle + tooth_angle))
        
        # Tip arc
        tip_start_angle = math.atan2(right_flank[-1][1], right_flank[-1][0]) + angle + tooth_angle
        tip_end_angle = math.atan2(left_flank[-1][1], left_flank[-1][0]) + angle + tooth_angle
        
        n_tip = 3
        for j in range(1, n_tip):
            a = tip_start_angle + (tip_end_angle - tip_start_angle) * j / n_tip
            all_points.append((tip_r * math.cos(a), tip_r * math.sin(a)))
    
    return all_points

# Build gear profile points
pts = build_gear_profile(num_teeth, pitch_radius, base_radius, tip_radius, root_radius)

# Create gear using polygon approximation via wire
# Use a simpler approach: create gear teeth using polar arrays of rounded rectangles cut into cylinder

# Simple gear approximation: cylinder with tooth bumps
# Create base cylinder at tip radius
gear_base = cq.Workplane("XY").cylinder(gear_height, tip_radius)

# Create tooth slots by cutting between teeth
# Each slot is a rounded rectangle cut
tooth_angle = 360.0 / num_teeth
slot_width = 2 * math.pi * root_radius / num_teeth * 0.45
slot_depth = addendum + dedendum

result_gear = gear_base
for i in range(num_teeth):
    angle = i * tooth_angle
    # Cut slot between teeth
    slot_x = (root_radius + slot_depth/2) * math.cos(math.radians(angle + tooth_angle/2))
    slot_y = (root_radius + slot_depth/2) * math.sin(math.radians(angle + tooth_angle/2))
    
    result_gear = (result_gear
        .cut(
            cq.Workplane("XY")
            .transformed(offset=cq.Vector(slot_x, slot_y, 0), rotate=cq.Vector(0, 0, angle + tooth_angle/2))
            .rect(slot_width, slot_depth * 2)
            .extrude(gear_height)
            .translate((0, 0, -gear_height/2))
        )
    )

# Add hub (base cylinder)
hub = cq.Workplane("XY").cylinder(hub_height + gear_height, hub_radius).translate((0, 0, -(hub_height)/2))

result = (result_gear
    .union(hub)
    .cut(cq.Workplane("XY").cylinder(gear_height + hub_height + 10, bore_radius))
)