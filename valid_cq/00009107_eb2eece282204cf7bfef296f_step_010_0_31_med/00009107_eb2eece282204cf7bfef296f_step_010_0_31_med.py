import cadquery as cq
import math

# Parameters
L = 100.0   # Length from center of large arc to center of small arc
R1 = 8.0    # Radius of the large end
R2 = 1.5    # Radius of the small end
T = 2.0     # Thickness
S = 5.0     # Side length of the square hole

# Calculate tangent points for the outer profile
alpha = math.asin((R1 - R2) / L)

# Top and bottom tangent points for both circles
p_t1 = (-R1 * math.sin(alpha), R1 * math.cos(alpha))
p_t2 = (-L - R2 * math.sin(alpha), R2 * math.cos(alpha))
p_b2 = (-L - R2 * math.sin(alpha), -R2 * math.cos(alpha))
p_b1 = (-R1 * math.sin(alpha), -R1 * math.cos(alpha))

# Midpoints for the three-point arcs
p_c2_mid = (-L - R2, 0)
p_c1_mid = (R1, 0)

# Create the main body
body = (
    cq.Workplane("XY")
    .moveTo(*p_t1)
    .lineTo(*p_t2)
    .threePointArc(p_c2_mid, p_b2)
    .lineTo(*p_b1)
    .threePointArc(p_c1_mid, p_t1)
    .close()
    .extrude(T)
)

# Create the square hole tool at the center of the large arc (origin)
hole = cq.Workplane("XY").rect(S, S).extrude(T)

# Cut the hole from the main body
result = body.cut(hole)