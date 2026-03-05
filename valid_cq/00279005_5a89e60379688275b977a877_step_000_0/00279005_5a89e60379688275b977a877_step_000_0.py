import cadquery as cq
import math

# --- Parametric Dimensions ---
# All units in mm
length_overall = 160.0
width_grip = 20.0
width_gauge = 10.0
length_gauge = 60.0  # Length of the parallel narrow section
radius_fillet = 30.0
thickness = 4.0

# --- Calculations for Geometry ---
# Calculate the X offset required for the transition arc.
# The arc is tangent to the narrow gauge section and intersects the grip section.
# y_step is the vertical distance between the grip edge and gauge edge.
y_step = (width_grip - width_gauge) / 2.0

# Ensure the radius is physically possible for the given step
if radius_fillet < y_step:
    raise ValueError("Fillet radius must be greater than the width step size.")

# Using circle equation x^2 + y^2 = r^2 derived logic for horizontal distance
x_transition = math.sqrt(radius_fillet**2 - (radius_fillet - y_step)**2)

# Key X coordinates (distance from center)
x_gauge_end = length_gauge / 2.0
x_grip_start = x_gauge_end + x_transition
x_end = length_overall / 2.0

# Key Y coordinates (distance from center line)
y_gauge = width_gauge / 2.0
y_grip = width_grip / 2.0

# --- Modeling ---

# Define the points for the top-half profile (Y > 0), moving Left to Right
p_start = (-x_end, 0)
p_grip_left_top = (-x_end, y_grip)
p_trans_left_start = (-x_grip_start, y_grip)
p_gauge_left_start = (-x_gauge_end, y_gauge)
p_gauge_right_end = (x_gauge_end, y_gauge)
p_trans_right_end = (x_grip_start, y_grip)
p_grip_right_top = (x_end, y_grip)
p_end = (x_end, 0)

# Create the sketch for the top half
# We use radiusArc for the smooth transitions. 
# A positive radius in CadQuery places the center of the arc to the 'left' of the drawing path.
# Since we traverse Left->Right and the curve center is 'Above' (higher Y), it is on the Left.
top_half = (
    cq.Workplane("XY")
    .moveTo(*p_start)
    .lineTo(*p_grip_left_top)
    .lineTo(*p_trans_left_start)
    .radiusArc(p_gauge_left_start, radius_fillet)
    .lineTo(*p_gauge_right_end)
    .radiusArc(p_trans_right_end, radius_fillet)
    .lineTo(*p_grip_right_top)
    .lineTo(*p_end)
    .close()
    .extrude(thickness)
)

# Mirror the top half about the XZ plane (which flips Y) to create the full symmetric object
result = top_half.union(top_half.mirror("XZ"))