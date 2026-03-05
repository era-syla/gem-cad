import cadquery as cq
import math

# --- Parametric Dimensions (based on standard ASTM D638 Type I geometry) ---
total_length = 165.0      # Total length of the specimen
grip_width = 19.0         # Width of the wider grip ends
gauge_width = 13.0        # Width of the narrow parallel gauge section
gauge_length = 57.0       # Length of the narrow parallel section
fillet_radius = 76.0      # Radius of the transition curve
thickness = 3.2           # Extrusion thickness

# --- Geometry Calculations ---
# Calculate the horizontal distance required for the transition arc.
# The arc is tangent to the narrow gauge section and intersects the wider grip section.
# dy is the step size from the gauge edge to the grip edge.
dy = (grip_width - gauge_width) / 2.0

# Validate that the radius is large enough to span the width difference
if fillet_radius <= dy:
    raise ValueError(f"Fillet radius ({fillet_radius}) must be larger than half the width difference ({dy}).")

# Using Pythagoras on the triangle formed by the radius center and the transition step:
# dx^2 + (R - dy)^2 = R^2
transition_dx = math.sqrt(fillet_radius**2 - (fillet_radius - dy)**2)

# Define key X and Y coordinates (symmetric around origin)
x_gauge_half = gauge_length / 2.0
x_grip_start = x_gauge_half + transition_dx
x_end = total_length / 2.0

y_gauge = gauge_width / 2.0
y_grip = grip_width / 2.0

# --- Model Generation ---
# Trace the outline Counter-Clockwise starting from Top-Right
result = (
    cq.Workplane("XY")
    .moveTo(x_end, y_grip)                          # Start: Top-Right Corner
    .lineTo(x_grip_start, y_grip)                   # Line: Top-Right Grip Edge
    
    # Arc: Top-Right Transition
    # Using negative radius for a clockwise arc segment (fillet shape)
    .radiusArc((x_gauge_half, y_gauge), -fillet_radius)
    
    .lineTo(-x_gauge_half, y_gauge)                 # Line: Top Gauge Section
    
    # Arc: Top-Left Transition
    .radiusArc((-x_grip_start, y_grip), -fillet_radius)
    
    .lineTo(-x_end, y_grip)                         # Line: Top-Left Grip Edge
    .lineTo(-x_end, -y_grip)                        # Line: Left End
    .lineTo(-x_grip_start, -y_grip)                 # Line: Bottom-Left Grip Edge
    
    # Arc: Bottom-Left Transition
    .radiusArc((-x_gauge_half, -y_gauge), -fillet_radius)
    
    .lineTo(x_gauge_half, -y_gauge)                 # Line: Bottom Gauge Section
    
    # Arc: Bottom-Right Transition
    .radiusArc((x_grip_start, -y_grip), -fillet_radius)
    
    .lineTo(x_end, -y_grip)                         # Line: Bottom-Right Grip Edge
    .close()                                        # Close profile (Right End)
    .extrude(thickness)                             # Create Solid
)