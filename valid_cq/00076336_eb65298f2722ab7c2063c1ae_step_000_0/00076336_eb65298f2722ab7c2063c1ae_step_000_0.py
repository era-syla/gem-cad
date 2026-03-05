import cadquery as cq

# --- Parametric Dimensions ---
# Base Plate
plate_width = 60.0
plate_height = 60.0
plate_thickness = 5.0
plate_fillet = 4.0

# Mounting Holes
hole_spacing_x = 42.0
hole_spacing_y = 42.0
hole_diameter = 5.0

# Arm
arm_length = 110.0
arm_width = 18.0
arm_rect_height = 12.0  # Height of the straight vertical part
arm_radius = arm_width / 2.0
arm_total_height = arm_rect_height + arm_radius

# End Stop
stop_thickness = 4.0
stop_protrusion = 10.0  # Height extending above the arm
stop_total_height = arm_total_height + stop_protrusion
stop_rect_height = stop_total_height - arm_radius

# --- Modeling ---

# 1. Create Base Plate
# Oriented on XY plane, extruded in Z
result = (
    cq.Workplane("XY")
    .box(plate_width, plate_height, plate_thickness)
    .edges("|Z").fillet(plate_fillet)
)

# 2. Add Mounting Holes
result = (
    result.faces(">Z").workplane()
    .rect(hole_spacing_x, hole_spacing_y, forConstruction=True)
    .vertices()
    .hole(hole_diameter)
)

# 3. Create Arm
# Draw D-profile (flat bottom, rounded top) on the face of the plate
# Calculate offset to center the arm vertically on the plate
y_offset_arm = -arm_total_height / 2.0

result = (
    result.faces(">Z").workplane()
    .center(0, y_offset_arm)  # Shift origin to the bottom of where the arm will be
    .moveTo(-arm_radius, 0)
    .lineTo(arm_radius, 0)
    .lineTo(arm_radius, arm_rect_height)
    .threePointArc((0, arm_rect_height + arm_radius), (-arm_radius, arm_rect_height))
    .close()
    .extrude(arm_length)
)

# 4. Create End Stop
# Draw taller D-profile on the end face of the arm
# Use CenterOfBoundBox to ensure (0,0) is the visual center of the arm end face (which aligns with plate center)
result = (
    result.faces(">Z").workplane(centerOption="CenterOfBoundBox")
    .moveTo(-arm_radius, y_offset_arm) # Start at the same bottom Y level relative to center
    .lineTo(arm_radius, y_offset_arm)
    .lineTo(arm_radius, y_offset_arm + stop_rect_height)
    .threePointArc((0, y_offset_arm + stop_rect_height + arm_radius), (-arm_radius, y_offset_arm + stop_rect_height))
    .close()
    .extrude(stop_thickness)
)