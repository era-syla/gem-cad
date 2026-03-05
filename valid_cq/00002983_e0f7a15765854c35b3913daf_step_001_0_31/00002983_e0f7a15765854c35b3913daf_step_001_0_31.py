import cadquery as cq
import math

# Parametric dimensions
L = 100.0       # Total length
W = 40.0        # Total width at the base
H = 20.0        # Total height
w_top = 20.0    # Width of the top section
h_flange = 4.0  # Height of the bottom flange part

# Derived radius for the concave fillets to ensure perfect tangency
R = (W - w_top) / 2.0

# Calculate midpoints for the 3-point arcs to create exact circular fillets
# Right arc midpoint
mid_x_r = W/2 - R * math.sqrt(2)/2
mid_y_r = h_flange + R - R * math.sqrt(2)/2

# Left arc midpoint
mid_x_l = -W/2 + R * math.sqrt(2)/2
mid_y_l = h_flange + R - R * math.sqrt(2)/2

# Construct the 2D profile on the XZ plane and extrude it
result = (
    cq.Workplane("XZ")
    .moveTo(-W/2, 0)
    .lineTo(W/2, 0)
    .lineTo(W/2, h_flange)
    .threePointArc((mid_x_r, mid_y_r), (w_top/2, h_flange + R))
    .lineTo(w_top/2, H)
    .lineTo(-w_top/2, H)
    .lineTo(-w_top/2, h_flange + R)
    .threePointArc((mid_x_l, mid_y_l), (-W/2, h_flange))
    .close()
    .extrude(L)
)