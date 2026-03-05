import cadquery as cq
import math

# --- Parameters ---
radius = 30.0          # Main body radius
thickness = 15.0       # Thickness of the main extrusion
fin_top_y = 50.0       # Y-coordinate of the top flat edge
fin_tip_x = 60.0       # X-coordinate of the right-most tip
fin_back_x = -10.0     # X-coordinate of the vertical cut on the left
hole_dia = 5.0         # Diameter of the through holes
hole_dist = 12.0       # Distance between the two holes
shaft_dia = 8.0        # Diameter of the rear shaft
shaft_len = 10.0       # Length of the rear shaft

# --- Geometry Calculations ---

# 1. Calculate the intersection of the vertical back line (x = fin_back_x) and the circle
# Circle eq: x^2 + y^2 = r^2 -> y = sqrt(r^2 - x^2)
p_start_y = math.sqrt(radius**2 - fin_back_x**2)
p_start = (fin_back_x, p_start_y)

# 2. Top-left corner of the fin
p_corner = (fin_back_x, fin_top_y)

# 3. Tip of the fin
p_tip = (fin_tip_x, fin_top_y)

# 4. Calculate the tangent point from the tip to the circle
# Distance and angle to the tip point
dist_tip = math.sqrt(fin_tip_x**2 + fin_top_y**2)
angle_tip = math.atan2(fin_top_y, fin_tip_x)

# The angle offset to the tangent point: cos(offset) = R / dist
angle_offset = math.acos(radius / dist_tip)

# Tangent angle (lower tangent line)
angle_tan = angle_tip - angle_offset
p_tan = (radius * math.cos(angle_tan), radius * math.sin(angle_tan))

# 5. Intermediate point for the arc (Midpoint on the circle for the return path)
# We need to traverse from the tangent point (approx 4th quadrant) to the start point (2nd quadrant)
# passing through the bottom/left. (-radius, 0) is a safe intermediate point.
p_arc_mid = (-radius, 0.0)

# --- Modeling ---

# Create the main body
# Outline: Start at circle intersection -> Vertical Up -> Horizontal Right -> Diagonal to Tangent -> Arc back to Start
main_body = (
    cq.Workplane("XY")
    .moveTo(*p_start)
    .lineTo(*p_corner)
    .lineTo(*p_tip)
    .lineTo(*p_tan)
    .threePointArc(p_arc_mid, p_start)
    .close()
    .extrude(thickness)
)

# Create the holes
# Positioning them slightly off-center to match the visual mass distribution
holes_x_start = 5.0
main_body = (
    main_body.faces(">Z")
    .workplane()
    .pushPoints([(holes_x_start, 0), (holes_x_start + hole_dist, 0)])
    .hole(hole_dia)
)

# Create the rear shaft
# Centered at origin, extruding in negative Z
shaft = (
    cq.Workplane("XY")
    .circle(shaft_dia / 2.0)
    .extrude(-shaft_len)
)

# Combine parts
result = main_body.union(shaft)