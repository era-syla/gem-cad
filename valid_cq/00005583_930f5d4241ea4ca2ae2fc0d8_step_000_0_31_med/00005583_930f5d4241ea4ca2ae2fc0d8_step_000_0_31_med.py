import cadquery as cq
import math

# Parametric dimensions
L = 120
L1 = 15
L2 = 105
Ro = 25
Ri = 20

# Angles in degrees for the radial cuts
t_top = 45
t_bot_near = -135
t_bot_far = -75

def make_profile(t_start, t_end):
    """
    Creates the C-shaped 2D profile for the tube section.
    Extrudes it along the X-axis (from the YZ plane).
    """
    if t_end <= t_start:
        t_end += 360
    
    t_start_rad = math.radians(t_start)
    t_end_rad = math.radians(t_end)
    
    p_out_start = (Ro * math.cos(t_start_rad), Ro * math.sin(t_start_rad))
    p_in_start = (Ri * math.cos(t_start_rad), Ri * math.sin(t_start_rad))
    p_in_end = (Ri * math.cos(t_end_rad), Ri * math.sin(t_end_rad))
    p_out_end = (Ro * math.cos(t_end_rad), Ro * math.sin(t_end_rad))
    
    mid_t = (t_start_rad + t_end_rad) / 2
    
    p_in_mid = (Ri * math.cos(mid_t), Ri * math.sin(mid_t))
    p_out_mid = (Ro * math.cos(mid_t), Ro * math.sin(mid_t))
    
    return (
        cq.Workplane("YZ")
        .moveTo(*p_out_start)
        .lineTo(*p_in_start)
        .threePointArc(p_in_mid, p_in_end)
        .lineTo(*p_out_end)
        .threePointArc(p_out_mid, p_out_start)
        .close()
    )

# Create the near segment (with the extended bottom lip)
part1 = make_profile(t_bot_near, t_top).extrude(L1)

# Create the far segment (stepped cut)
part2 = make_profile(t_bot_far, t_top).extrude(L2).translate((L1, 0, 0))

# Combine the segments
result = part1.union(part2)

# Create the side hole along the stepped edge of the far segment
R_mid = (Ro + Ri) / 2
hole_x_pos = L - 20
hole_center = cq.Vector(
    hole_x_pos, 
    R_mid * math.cos(math.radians(t_bot_far)), 
    R_mid * math.sin(math.radians(t_bot_far))
)

# The hole is drilled normal to the radial cut face, into the material
hole_dir = cq.Vector(
    0, 
    math.cos(math.radians(t_bot_far + 90)), 
    math.sin(math.radians(t_bot_far + 90))
)

# Create the cutting cylinder
hole = cq.Solid.makeCylinder(3, 20, pnt=hole_center - hole_dir * 5, dir=hole_dir)

# Subtract the hole
result = result.cut(hole)