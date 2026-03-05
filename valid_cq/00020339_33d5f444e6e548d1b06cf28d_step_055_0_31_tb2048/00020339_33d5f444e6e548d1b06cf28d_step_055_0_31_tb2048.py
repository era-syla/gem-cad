import cadquery as cq
import math

# Parameters
R_center = 20.0
H_center = 18.0

Dist_right = 38.0
R_right = 11.0
H_right = 15.0

Dist_left = 28.0
R_left = 13.0
H_left = 4.0

R_hole = 3.0

def make_arm(R1, R2, D, H, direction="right"):
    """
    Creates an arm with a tangent web connecting to the central cylinder.
    """
    # Angle for the tangent lines
    alpha = math.asin((R1 - R2) / D)
    sign = 1 if direction == "right" else -1
    
    # Calculate tangent points
    x1 = R1 * math.sin(alpha) * sign
    y1 = R1 * math.cos(alpha)
    
    x2 = (D + R2 * math.sin(alpha)) * sign
    y2 = R2 * math.cos(alpha)
    
    x3 = x2
    y3 = -y2
    
    x4 = x1
    y4 = -y1
    
    # Create the connecting web
    pts = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
    web = cq.Workplane("XY").polyline(pts).close().extrude(H)
    
    # Create the outer cylinder of the arm
    end_cyl = cq.Workplane("XY").center(D * sign, 0).circle(R2).extrude(H)
    
    return web.union(end_cyl)

# Create the main central cylinder
result = cq.Workplane("XY").circle(R_center).extrude(H_center)

# Create and union the right and left arms
right_arm = make_arm(R_center, R_right, Dist_right, H_right, "right")
left_arm = make_arm(R_center, R_left, Dist_left, H_left, "left")

result = result.union(right_arm).union(left_arm)

# Create the through hole in the center and cut it from the solid
hole = cq.Workplane("XY").circle(R_hole).extrude(H_center)
result = result.cut(hole)