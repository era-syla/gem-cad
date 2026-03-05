import cadquery as cq
import math

# --- Parameters ---
r_inner = 60.0          # Inner radius of the curved segment
width = 25.0            # Radial width (thickness) at the top
height = 25.0           # Vertical height of the inner face
angle = 70.0            # Total angular span of the segment (degrees)
pin_diam = 4.0          # Diameter of the central pin
pin_len = 8.0           # Length of the pin protruding from surface
hole_diam = 5.0         # Diameter of the side holes
hole_angle = 20.0       # Angular offset for holes from the center

# --- 1. Create Main Body ---
# Define profile in XZ plane to be revolved around Z axis.
# Profile: Vertical inner edge, Horizontal top edge, Curved outer edge connecting top-outer to bottom-inner.
# The profile is defined in the XZ plane, where local X corresponds to radial distance, and local Y to Z height.

# Points for the profile
p_inner_bottom = (r_inner, 0)
p_inner_top = (r_inner, height)
p_outer_top = (r_inner + width, height)

# Calculate a midpoint for the outer arc (assuming a quarter-circle profile tangent to top)
# Center of arc at (r_inner, height), radius = width
theta_mid = math.radians(-45)
p_arc_mid_x = r_inner + width * math.cos(theta_mid)
p_arc_mid_y = height + width * math.sin(theta_mid)
p_arc_mid = (p_arc_mid_x, p_arc_mid_y)

# Construct the profile and revolve
body = (
    cq.Workplane("XZ")
    .moveTo(*p_inner_bottom)
    .lineTo(*p_inner_top)
    .lineTo(*p_outer_top)
    .threePointArc(p_arc_mid, p_inner_bottom)
    .close()
    .revolve(angle)
)

# Center the revolved body on the Y-axis (revolve starts at 0)
body = body.rotate((0, 0, 0), (0, 0, 1), -angle / 2.0)

# --- 2. Create Central Pin ---
# Create a pin on the inner concave face (radius = r_inner)
# Position: Centered vertically (z=height/2) and angularly (angle=0)
# Orientation: Pointing inwards (towards the origin)
pin = (
    cq.Workplane("YZ")
    .workplane(offset=r_inner)
    .center(0, height / 2.0)
    .circle(pin_diam / 2.0)
    .extrude(-pin_len)  # Negative extrusion to point into the empty center space
)

# --- 3. Create Side Holes ---
# Helper function to create a cutter object for the holes
def create_hole_cutter(angle_offset):
    # Create a cylinder starting at the inner face and going outwards into the body
    cutter = (
        cq.Workplane("YZ")
        .workplane(offset=r_inner)
        .center(0, height / 2.0)
        .circle(hole_diam / 2.0)
        .extrude(width * 1.5)  # Extrude deep enough to cut through the tapering body
    )
    # Rotate the cutter to the specified angle
    return cutter.rotate((0, 0, 0), (0, 0, 1), angle_offset)

# Create cutters for left and right holes
hole_left = create_hole_cutter(hole_angle)
hole_right = create_hole_cutter(-hole_angle)

# --- 4. Final Boolean Operations ---
result = body.union(pin).cut(hole_left).cut(hole_right)