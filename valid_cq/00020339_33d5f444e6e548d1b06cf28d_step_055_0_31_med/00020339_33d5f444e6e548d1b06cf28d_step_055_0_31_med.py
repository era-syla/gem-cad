import cadquery as cq
import math

# Parametric dimensions
R_hub = 20.0       # Radius of the central hub
H_hub = 15.0       # Height of the central hub

L_thick = 35.0     # Distance from center to thick arm center
R_thick = 12.0     # Radius of the thick arm end
H_thick = 15.0     # Height of the thick arm (matches hub)

L_thin = 25.0      # Distance from center to thin arm center
R_thin = 15.0      # Radius of the thin arm end
H_thin = 4.0       # Height of the thin arm

R_hole = 4.0       # Radius of the center hole

def make_arm(r_hub, r_arm, L, height, direction=1):
    """
    Creates an arm with a tangent trapezoid connecting the hub to the arm end.
    direction=1 creates the arm along +X, direction=-1 along -X.
    """
    # Calculate the angle for the tangent lines
    theta = math.asin((r_hub - r_arm) / L)
    sin_t = math.sin(theta)
    cos_t = math.cos(theta)
    
    # Calculate tangent contact points
    p1 = (r_hub * sin_t * direction, r_hub * cos_t)
    p2 = ((L + r_arm * sin_t) * direction, r_arm * cos_t)
    p3 = ((L + r_arm * sin_t) * direction, -r_arm * cos_t)
    p4 = (r_hub * sin_t * direction, -r_hub * cos_t)
    
    # Create the connecting trapezoidal body
    trap = (
        cq.Workplane("XY")
        .polyline([p1, p2, p3, p4])
        .close()
        .extrude(height)
    )
    
    # Create the cylindrical end of the arm
    cyl = (
        cq.Workplane("XY")
        .center(L * direction, 0)
        .circle(r_arm)
        .extrude(height)
    )
    
    return trap.union(cyl)

# 1. Create central hub
hub = cq.Workplane("XY").circle(R_hub).extrude(H_hub)

# 2. Create the two arms
thick_arm = make_arm(R_hub, R_thick, L_thick, H_thick, direction=1)
thin_arm = make_arm(R_hub, R_thin, L_thin, H_thin, direction=-1)

# 3. Combine all parts into a single solid
result = hub.union(thick_arm).union(thin_arm)

# 4. Cut the center through-hole
# Creating a cutter cylinder slightly longer than the max height to ensure a clean cut
hole_cutter = (
    cq.Workplane("XY")
    .workplane(offset=-5)
    .circle(R_hole)
    .extrude(H_hub + 10)
)

result = result.cut(hole_cutter)