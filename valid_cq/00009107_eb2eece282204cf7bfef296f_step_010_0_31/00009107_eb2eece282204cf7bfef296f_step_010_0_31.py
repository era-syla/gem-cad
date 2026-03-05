import cadquery as cq
import math

# Parametric dimensions
L = 120.0            # Total length from circular center to flat tip
R = 12.0             # Radius of the large rounded end
h = 2.0              # Half-width of the narrow flat tip
thickness = 1.5      # Thickness of the part
hole_size = 5.0      # Side length of the square hole
tip_fillet = 0.5     # Fillet radius at the narrow tip corners

# Calculate top tangent point from the tip corner (L, h) to the circle at (0,0) with radius R
# This ensures perfectly smooth mathematical continuity between the straight edges and the back arc
A_val = L**2 + h**2
sqrt_term = math.sqrt(L**2 + h**2 - R**2)
x_top = (R**2 * L - R * h * sqrt_term) / A_val
y_top = (R**2 - x_top * L) / h

# Bottom tangent point (symmetric across X-axis)
x_bot = x_top
y_bot = -y_top

# Create the 2D profile with the outer wedge shape and the inner square hole
profile = (
    cq.Workplane("XY")
    .moveTo(x_top, y_top)
    .lineTo(L, h)
    .lineTo(L, -h)
    .lineTo(x_bot, y_bot)
    .threePointArc((-R, 0), (x_top, y_top))
    .close()
    .moveTo(0, 0)
    .rect(hole_size, hole_size)
)

# Extrude into a 3D solid
result = profile.extrude(thickness)

# Fillet the sharp vertical edges at the narrow tip for a finished look
# .edges("|Z") selects edges parallel to Z (thickness)
# .edges(">X") isolates the edges at the very tip (furthest along positive X)
result = result.edges("|Z").edges(">X").fillet(tip_fillet)