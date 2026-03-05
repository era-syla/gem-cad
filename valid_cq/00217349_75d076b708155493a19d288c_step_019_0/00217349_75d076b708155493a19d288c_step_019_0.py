import cadquery as cq

# -----------------------------------------------------------------------------
# Parametric Dimensions
# -----------------------------------------------------------------------------
base_outer_diameter = 20.0
base_inner_diameter = 12.0
base_height = 35.0

arm_width = 4.0        # Cross-section width (Y direction)
arm_thickness = 4.0    # Cross-section thickness (Radial/X direction)
arm_height = 40.0      # Height of the arm extending above the base cylinder
overhang_length = 6.0  # Length of the top horizontal segment

pin_diameter = 1.5
pin_length = 1.5

# -----------------------------------------------------------------------------
# Geometry Construction
# -----------------------------------------------------------------------------

# 1. Create the base hollow cylinder (Tube)
base = (
    cq.Workplane("XY")
    .circle(base_outer_diameter / 2.0)
    .circle(base_inner_diameter / 2.0)
    .extrude(base_height)
)

# 2. Create the vertical segment of the arm
# Positioned on top of the cylinder wall, aligned with the outer edge
arm_center_x = (base_outer_diameter / 2.0) - (arm_thickness / 2.0)

vertical_arm = (
    cq.Workplane("XY")
    .workplane(offset=base_height)
    .center(arm_center_x, 0)
    .rect(arm_thickness, arm_width)
    .extrude(arm_height)
)

# 3. Create the horizontal segment of the arm (L-shape overhang)
# This sits at the top of the vertical arm and extends inwards towards the center
# We calculate coordinates to ensure a clean geometric junction
# Start X (inner edge of vertical arm):
start_x = arm_center_x - (arm_thickness / 2.0)
# Center X for the new segment:
overhang_center_x = start_x - (overhang_length / 2.0)
# Z level for the sketch (top of structure minus thickness):
overhang_z_level = base_height + arm_height - arm_thickness

horizontal_arm = (
    cq.Workplane("XY")
    .workplane(offset=overhang_z_level)
    .center(overhang_center_x, 0)
    .rect(overhang_length, arm_width)
    .extrude(arm_thickness)
)

# 4. Create the small pin at the tip
# The pin is located on the innermost face of the overhang, pointing inwards
pin_face_x = start_x - overhang_length
pin_center_z = overhang_z_level + (arm_thickness / 2.0)

pin = (
    cq.Workplane("YZ")
    .workplane(offset=pin_face_x)
    .center(0, pin_center_z)
    .circle(pin_diameter / 2.0)
    .extrude(-pin_length)  # Extrude along negative X axis (towards center)
)

# 5. Combine all solids into the final result
result = base.union(vertical_arm).union(horizontal_arm).union(pin)