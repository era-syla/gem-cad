import cadquery as cq
import math

# -----------------------------------------------------------------------------
# Dogbone Tensile Specimen Parameters
# -----------------------------------------------------------------------------
total_length = 160.0    # Total length of the specimen
grip_width = 20.0       # Width of the wider grip sections
gauge_width = 10.0      # Width of the narrow gauge section
gauge_length = 50.0     # Length of the parallel gauge section
thickness = 6.0         # Thickness of the plate
fillet_radius = 25.0    # Radius of the transition fillet

# -----------------------------------------------------------------------------
# Geometry Calculations
# -----------------------------------------------------------------------------
# Calculate the horizontal length of the transition arc.
# The arc is tangent to the gauge section (horizontal) and intersects the grip section.
# Arc Center Y = (gauge_width / 2) + fillet_radius
# Intersect Y = grip_width / 2
# We solve for dx in the circle equation.

y_gauge_half = gauge_width / 2.0
y_grip_half = grip_width / 2.0
y_arc_center = y_gauge_half + fillet_radius

# Vertical distance from arc center to the intersection line
dy = y_grip_half - y_arc_center

# Horizontal distance (dx) from the start of the arc (tangent point) to the end
transition_dx = math.sqrt(fillet_radius**2 - dy**2)

# Define key points for the top-right quadrant profile
p_origin = (0, 0)
p_gauge_start = (0, y_gauge_half)
p_arc_start = (gauge_length / 2.0, y_gauge_half)
p_arc_end = (gauge_length / 2.0 + transition_dx, y_grip_half)
p_grip_end = (total_length / 2.0, y_grip_half)
p_corner_bottom = (total_length / 2.0, 0)

# -----------------------------------------------------------------------------
# Modeling
# -----------------------------------------------------------------------------

# Create the top-right quadrant using a sketch
# We draw from the gauge outwards to ensure the arc is tangent to the gauge section
quadrant = (
    cq.Workplane("XY")
    .moveTo(*p_origin)
    .lineTo(*p_gauge_start)
    .lineTo(*p_arc_start)
    .tangentArcPoint(p_arc_end)  # Create arc tangent to previous line (horizontal)
    .lineTo(*p_grip_end)
    .lineTo(*p_corner_bottom)
    .close()
    .extrude(thickness)
)

# Mirror to create the full geometry
# 1. Mirror about XZ plane (flips Y axis) to create the right half
right_half = quadrant.union(quadrant.mirror("XZ"))

# 2. Mirror about YZ plane (flips X axis) to create the full part
result = right_half.union(right_half.mirror("YZ"))