import cadquery as cq
import math

# Parameters
gear_thickness = 8
belt_thickness = 4
belt_width = 8

# Three gear positions forming a triangle
# Large gear at top-right, two smaller gears at bottom
large_gear_r = 30
small_gear_r = 18
small_gear2_r = 18

# Positions
pos_large = (60, 120, 0)
pos_small1 = (0, 0, 0)
pos_small2 = (80, 0, 0)

def make_gear(outer_r, inner_r, num_teeth, thickness, bore_r=5):
    """Create a spur gear approximation"""
    tooth_height = (outer_r - inner_r) * 0.4
    pitch_r = inner_r + tooth_height
    
    # Base disk
    gear = cq.Workplane("XY").circle(inner_r).extrude(thickness)
    
    # Add teeth
    for i in range(num_teeth):
        angle = 360.0 / num_teeth * i
        rad = math.radians(angle)
        tx = math.cos(rad) * (inner_r + tooth_height/2)
        ty = math.sin(rad) * (inner_r + tooth_height/2)
        
        tooth_w = 2 * math.pi * inner_r / num_teeth * 0.45
        tooth_h = tooth_height
        
        tooth = (cq.Workplane("XY")
                 .center(tx, ty)
                 .rect(tooth_w, tooth_h)
                 .extrude(thickness))
        
        # Rotate the tooth to align radially
        tooth = tooth.rotate((tx, ty, 0), (tx, ty, thickness), 0)
        
        gear = gear.union(tooth)
    
    # Add hub cutouts for large gear
    if outer_r > 25:
        hub_r = inner_r * 0.65
        for i in range(5):
            angle = 360.0 / 5 * i
            rad = math.radians(angle)
            hx = math.cos(rad) * hub_r * 0.6
            hy = math.sin(rad) * hub_r * 0.6
            hole = (cq.Workplane("XY")
                    .center(hx, hy)
                    .circle(hub_r * 0.3)
                    .extrude(thickness))
            gear = gear.cut(hole)
    
    # Center bore
    bore = cq.Workplane("XY").circle(bore_r).extrude(thickness)
    gear = gear.cut(bore)
    
    return gear

def make_simple_gear(outer_r, num_teeth, thickness, bore_r=4):
    """Simpler gear with rectangular teeth"""
    tooth_h = outer_r * 0.15
    base_r = outer_r - tooth_h
    
    gear = cq.Workplane("XY").circle(base_r).extrude(thickness)
    
    for i in range(num_teeth):
        angle = 360.0 / num_teeth * i
        rad = math.radians(angle)
        cx = math.cos(rad) * (base_r + tooth_h/2)
        cy = math.sin(rad) * (base_r + tooth_h/2)
        
        tooth_w = 2 * math.pi * base_r / num_teeth * 0.5
        
        pts = [
            (-tooth_w/2, -tooth_h/2),
            (tooth_w/2, -tooth_h/2),
            (tooth_w/2, tooth_h/2),
            (-tooth_w/2, tooth_h/2),
        ]
        tooth = (cq.Workplane("XY")
                 .center(cx, cy)
                 .rect(tooth_w, tooth_h)
                 .extrude(thickness)
                 .rotate((0,0,0),(0,0,1), math.degrees(rad)))
        gear = gear.union(tooth)
    
    bore = cq.Workplane("XY").circle(bore_r).extrude(thickness)
    gear = gear.cut(bore)
    return gear

# Create belt as a triangular loop connecting the three gears
def make_belt_segment(p1, p2, width, thickness):
    """Create a belt segment between two points"""
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    length = math.sqrt(dx*dx + dy*dy)
    angle = math.degrees(math.atan2(dy, dx))
    
    cx = (p1[0] + p2[0]) / 2
    cy = (p1[1] + p2[1]) / 2
    
    seg = (cq.Workplane("XY")
           .center(cx, cy)
           .rect(length, width)
           .extrude(thickness)
           .rotate((cx, cy, 0), (cx, cy, thickness), angle))
    return seg

# Gear positions
gp_large = (60, 120)
gp_s1 = (0, 0)
gp_s2 = (80, 0)

belt_z_offset = (gear_thickness - belt_thickness) / 2

# Belt segments
belt1 = make_belt_segment(gp_large, gp_s1, belt_width, belt_thickness)
belt2 = make_belt_segment(gp_large, gp_s2, belt_width, belt_thickness)
belt3 = make_belt_segment(gp_s1, gp_s2, belt_width, belt_thickness)

belt = belt1.union(belt2).union(belt3)
belt = belt.translate((0, 0, belt_z_offset))

# Large gear
lg = make_simple_gear(large_gear_r, 28, gear_thickness, bore_r=5)
lg = lg.translate((gp_large[0], gp_large[1], 0))

# Small gear 1
sg1 = make_simple_gear(small_gear_r, 20, gear_thickness, bore_r=4)
sg1 = sg1.translate((gp_s1[0], gp_s1[1], 0))

# Small gear 2
sg2 = make_simple_gear(small_gear2_r, 20, gear_thickness, bore_r=4)
sg2 = sg2.translate((gp_s2[0], gp_s2[1], 0))

# Combine all
result = belt.union(lg).union(sg1).union(sg2)