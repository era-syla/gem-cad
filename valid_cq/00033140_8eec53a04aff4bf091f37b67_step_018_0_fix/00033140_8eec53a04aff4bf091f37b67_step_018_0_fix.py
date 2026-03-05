import cadquery as cq
import math

# Parameters
L = 100       # triangle base length in X
H = 80        # triangle height in Y
D = 10        # plate thickness (extrusion in Z)

ridge_offset = 20    # distance along hypotenuse where ridge starts
ridge_len = 40       # length of ridge along hypotenuse
ridge_h = 10         # height of ridge above plate

notch_depth = 10     # how deep the notch cuts into X
notch_h = 20         # height of notch from top of plate

# 1) main triangular plate
result = cq.Workplane("XY").polyline([(0, 0), (L, 0), (0, H)]).close().extrude(D)

# 2) add ridge on the sloped (hypotenuse) edge
# compute unit vector along hypotenuse from (0,H) toward (L,0)
hyp_len = math.hypot(L, H)
ux, uy = L/hyp_len, -H/hyp_len
# midpoint along hypotenuse where ridge will be centered
mid_dist = ridge_offset + ridge_len/2
mx = 0 + ux*mid_dist
my = H + uy*mid_dist
# angle of hypotenuse in XY
angle = math.degrees(math.atan2(uy, ux))
# create ridge as a rectangular box, welded to top face
ridge = (
    cq.Workplane("XY")
    .transformed(offset=(mx, my, D), rotate=(0, 0, angle))
    .box(ridge_len, D, ridge_h, centered=(True, True, False))
)
result = result.union(ridge)

# 3) cut notch on the right vertical face
# create a block and subtract it
notch = (
    cq.Workplane("XY")
    .transformed(offset=(L - notch_depth, 0, D - notch_h))
    .box(notch_depth, D, notch_h, centered=(False, True, False))
)
result = result.cut(notch)