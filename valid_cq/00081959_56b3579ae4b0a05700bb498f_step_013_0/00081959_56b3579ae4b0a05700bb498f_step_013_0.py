import cadquery as cq

# --- Parametric Dimensions ---
plate_thickness = 10.0
arm_width = 60.0
arm_length = 180.0       # Total length from center to tip
hole_diameter = 10.0

# Hole layout parameters
hole_tip_margin = 20.0   # Distance from the tip of the arm to the first pair of holes
hole_row_spacing = 40.0  # Distance between the two rows of holes along the arm
hole_width_spacing = 35.0 # Distance between holes across the width of the arm

# --- Modeling ---

# 1. Create a single arm defined along the X-axis
# We create a box centered at origin, then translate it so one end is at the origin (center of the Y-plate)
# This results in an arm extending from x=0 to x=arm_length
arm_geo = (
    cq.Workplane("XY")
    .box(arm_length, arm_width, plate_thickness)
    .translate((arm_length / 2, 0, 0))
)

# 2. Define hole positions for the single arm
# Coordinates are calculated relative to the global origin since the arm is aligned with X-axis
x_outer = arm_length - hole_tip_margin
x_inner = x_outer - hole_row_spacing
y_offset = hole_width_spacing / 2

hole_points = [
    (x_outer, y_offset),
    (x_outer, -y_offset),
    (x_inner, y_offset),
    (x_inner, -y_offset)
]

# 3. Drill holes in the base arm
arm_with_holes = (
    arm_geo
    .faces(">Z")
    .workplane()
    .pushPoints(hole_points)
    .hole(hole_diameter)
)

# 4. Create the Y-shape by rotating and unioning the arm
# We keep the original, and unite it with copies rotated by 120 and 240 degrees around the Z-axis
arm0 = arm_with_holes
arm120 = arm_with_holes.rotate((0, 0, 0), (0, 0, 1), 120)
arm240 = arm_with_holes.rotate((0, 0, 0), (0, 0, 1), 240)

result = arm0.union(arm120).union(arm240)