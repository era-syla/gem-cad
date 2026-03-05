import cadquery as cq
import math

# --- Parameters ---
width = 100.0          # Chord width of the bottom arc
sagitta = 20.0         # Height of the arc (depth of curve)
leg_length = 45.0      # Length of the straight side sections
leg_angle = 12.0       # Angle of legs from vertical (degrees)
thickness = 3.0        # Thickness of the square wire profile

# --- Geometry Calculation ---
# Convert angle to radians for calculation
theta = math.radians(leg_angle)

# Calculate leg offsets (assuming inward tilt)
dx_leg = leg_length * math.sin(theta)
dy_leg = leg_length * math.cos(theta)

# Define key geometric points
p_arc_start = (-width / 2.0, 0.0)
p_arc_end   = (width / 2.0, 0.0)
p_arc_mid   = (0.0, -sagitta)

# Calculate leg tip points relative to arc ends
# Left leg starts at top and goes down to arc start
p_leg_left_top = (p_arc_start[0] + dx_leg, p_arc_start[1] + dy_leg)
# Right leg goes from arc end up to top
p_leg_right_top = (p_arc_end[0] - dx_leg, p_arc_end[1] + dy_leg)

# --- Modeling ---

# 1. Create the Sweep Path
# The path consists of a straight line, an arc, and another straight line
path = (
    cq.Workplane("XY")
    .moveTo(*p_leg_left_top)
    .lineTo(*p_arc_start)
    .threePointArc(p_arc_mid, p_arc_end)
    .lineTo(*p_leg_right_top)
)

# 2. Create the Profile and Sweep
# Define a workplane perpendicular to the start of the path (the left leg)
# The normal vector points along the first segment: from Top to Arc Start
path_start_normal = (-dx_leg, -dy_leg, 0)

profile_plane = cq.Workplane(cq.Plane(origin=p_leg_left_top, normal=path_start_normal))

# Draw the square profile on the custom plane and sweep it along the path
result = (
    profile_plane
    .rect(thickness, thickness)
    .sweep(path)
)