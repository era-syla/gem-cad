import cadquery as cq
import math

# ==========================================
# Parametric Dimensions (Dogbone Specimen)
# ==========================================
length_overall = 160.0      # Total length of the specimen
width_grip = 20.0           # Width of the wider grip sections
width_gauge = 10.0          # Width of the narrow gauge section
length_gauge = 60.0         # Length of the parallel gauge section
thickness = 4.0             # Thickness of the specimen
radius_transition = 50.0    # Radius of the transition curve

# ==========================================
# Geometric Calculations
# ==========================================
# Calculate the horizontal length (dx) of the transition zone.
# The arc is tangent to the gauge section and intersects the grip section.
# dy is the step height between the gauge and grip half-widths.
dy = (width_grip - width_gauge) / 2.0

# Validation: Radius must be larger than the step height
if radius_transition <= dy:
    # Fallback to a valid radius if the parameter is too small
    radius_transition = dy * 1.5

# Calculate x offset using Pythagoras on the fillet circle
# (R)^2 = (x_offset)^2 + (R - dy)^2
x_transition_len = math.sqrt(radius_transition**2 - (radius_transition - dy)**2)

# Define X coordinates for key transition points (relative to center)
x_gauge_end = length_gauge / 2.0
x_grip_start = x_gauge_end + x_transition_len

# ==========================================
# 3D Model Generation
# ==========================================
result = (
    cq.Workplane("XY")
    # Start at the center of the left edge
    .moveTo(-length_overall / 2.0, 0.0)
    
    # --- Construct Top Half of Profile ---
    # Line up to top-left corner
    .lineTo(-length_overall / 2.0, width_grip / 2.0)
    
    # Horizontal line for left grip
    .lineTo(-x_grip_start, width_grip / 2.0)
    
    # Concave arc transitioning to the gauge section
    # radiusArc(endPoint, radius): Negative radius creates a "sag" (concave) arc
    .radiusArc((-x_gauge_end, width_gauge / 2.0), -radius_transition)
    
    # Horizontal line for the gauge section
    .lineTo(x_gauge_end, width_gauge / 2.0)
    
    # Concave arc transitioning back to the grip section
    .radiusArc((x_grip_start, width_grip / 2.0), -radius_transition)
    
    # Horizontal line for right grip
    .lineTo(length_overall / 2.0, width_grip / 2.0)
    
    # Line down to the center of the right edge
    .lineTo(length_overall / 2.0, 0.0)
    
    # --- Mirror and Extrude ---
    # Mirror the top edges about the X-axis to create the bottom half and close the wire
    .mirrorX()
    
    # Extrude to create the solid geometry
    .extrude(thickness)
)