import cadquery as cq
import math

# --- Parameters ---
pitch = 40.0          # Distance between hole centers
end_radius = 12.0     # Radius of the rounded ends (width / 2)
hole_diameter = 10.0  # Diameter of the mounting holes
waist_width = 16.0    # Width of the narrowest middle section
thickness = 2.0       # Plate thickness

# --- Geometry Calculation ---
# Calculate the geometry for a "figure-8" chain link style plate.
# The shape consists of two end circles connected by concave arcs.
# We compute the radius of the side connecting arc (R_side) to ensure 
# perfect tangency with the end circles.

h = pitch / 2.0
e = end_radius
a = waist_width / 2.0

# Formula derived from geometric constraints for tangency:
# R_side is the radius of the concave arc on the side.
# (R + a)^2 + h^2 = (R + e)^2  --> derived from distance between centers
# R = (e^2 - a^2 - h^2) / (2 * (a - e))
r_side = (e**2 - a**2 - h**2) / (2 * (a - e))

# Center X coordinate of the side arc (centered at Y=0)
x_center = r_side + a

# Calculate the intersection point (tangency point) between the end circle and side arc.
# Vector from End Circle Center (0, h) to Side Arc Center (x_center, 0)
vec_x = x_center - 0
vec_y = 0 - h
dist_centers = math.sqrt(vec_x**2 + vec_y**2)

# The point on the end circle boundary along that vector:
# P = Center + Radius * (Vector / Length)
p_tr_x = 0 + e * (vec_x / dist_centers)
p_tr_y = h + e * (vec_y / dist_centers)

# Define the four symmetry points for the profile
p_tr = (p_tr_x, p_tr_y)   # Top-Right
p_tl = (-p_tr_x, p_tr_y)  # Top-Left
p_br = (p_tr_x, -p_tr_y)  # Bottom-Right
p_bl = (-p_tr_x, -p_tr_y) # Bottom-Left

# --- Modeling ---
result = (
    cq.Workplane("XY")
    .moveTo(*p_tl)
    # Top Arc: From Top-Left to Top-Right, passing through the top apex (0, h + e)
    .threePointArc((0, h + e), p_tr)
    # Right Side Arc: From Top-Right to Bottom-Right, passing through waist (a, 0)
    .threePointArc((a, 0), p_br)
    # Bottom Arc: From Bottom-Right to Bottom-Left, passing through bottom apex (0, -h - e)
    .threePointArc((0, -h - e), p_bl)
    # Left Side Arc: From Bottom-Left to Top-Left, passing through waist (-a, 0)
    .threePointArc((-a, 0), p_tl)
    .close()
    .extrude(thickness)
    # Create the holes at the pitch points
    .faces(">Z").workplane()
    .pushPoints([(0, h), (0, -h)])
    .hole(hole_diameter)
)