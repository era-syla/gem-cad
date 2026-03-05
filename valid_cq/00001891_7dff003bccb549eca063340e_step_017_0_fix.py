import cadquery as cq
import math

# Create a shuriken/throwing star with curved blades
# The shape has 8 curved blades radiating from a central hub

def make_blade_profile():
    """Create a single blade as a 2D wire"""
    pts = [
        (0, 0),
        (2, 1),
        (5, 0.5),
        (7, 2),
        (8, 4),
        (6, 3),
        (4, 2),
        (2, 3),
        (1, 2),
        (0, 0),
    ]
    return pts

# Build the 2D shuriken shape using splines for curved blades
# 8 blades rotated around center

def create_shuriken_2d():
    num_blades = 8
    
    # Create blade points (one blade)
    # Blade extends from center outward with a sweep
    r_inner = 1.5
    r_outer = 9.0
    
    all_points = []
    
    for i in range(num_blades):
        angle_start = i * (360 / num_blades)
        angle_rad = math.radians(angle_start)
        # Each blade: swept curved shape
        
    # Use polygon approach - create the shuriken as extruded profile
    # Build outline as series of points
    points = []
    num_blades = 8
    
    for i in range(num_blades):
        base_angle = i * (2 * math.pi / num_blades)
        # Trailing edge of blade (inner)
        a1 = base_angle
        # Tip of blade
        a2 = base_angle + math.pi / num_blades * 0.5
        # Leading edge sweep
        a3 = base_angle + math.pi / num_blades
        
        # Inner point
        x1 = r_inner * math.cos(a1)
        y1 = r_inner * math.sin(a1)
        
        # Outer tip (offset rotationally for swept look)
        tip_angle = base_angle - math.pi / num_blades * 1.2
        x2 = r_outer * math.cos(tip_angle)
        y2 = r_outer * math.sin(tip_angle)
        
        # Mid sweep point
        x3 = (r_inner + r_outer) * 0.4 * math.cos(base_angle - math.pi / num_blades * 0.3)
        y3 = (r_inner + r_outer) * 0.4 * math.sin(base_angle - math.pi / num_blades * 0.3)
        
        points.extend([(x1, y1), (x3, y3), (x2, y2)])
    
    return points

# Create shuriken using a different approach - draw individual blade shapes and union them
result = cq.Workplane("XY")

# Central hub
hub = cq.Workplane("XY").circle(2.0).extrude(1.5)

# Create blades
num_blades = 8
blade_union = hub

for i in range(num_blades):
    angle_deg = i * (360.0 / num_blades)
    angle_rad = math.radians(angle_deg)
    
    # Blade profile points (in local frame, blade along X axis)
    # Swept blade shape
    blade_pts = [
        (1.5, 0.3),
        (3.0, 0.8),
        (6.0, 1.5),
        (9.0, 0.5),
        (8.5, -0.3),
        (5.5, 0.2),
        (2.5, -0.5),
        (1.5, -0.3),
        (1.5, 0.3),
    ]
    
    # Rotate points by angle
    rotated_pts = []
    for (x, y) in blade_pts:
        xr = x * math.cos(angle_rad) - y * math.sin(angle_rad)
        yr = x * math.sin(angle_rad) + y * math.cos(angle_rad)
        rotated_pts.append((xr, yr))
    
    blade = (cq.Workplane("XY")
             .polyline(rotated_pts)
             .close()
             .extrude(1.0))
    
    blade_union = blade_union.union(blade)

result = blade_union