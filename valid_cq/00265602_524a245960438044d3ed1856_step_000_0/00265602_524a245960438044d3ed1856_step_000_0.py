import cadquery as cq

# --- Parameters ---
# Head dimensions (The curved block section)
head_width = 50.0       # Extrusion length (Y-axis)
head_profile_len = 35.0 # Chord length of the lens profile (X-axis)
head_profile_ht = 20.0  # Thickness of the lens profile (Z-axis)

# Arm dimensions (The flat strip)
arm_length = 90.0
arm_width = 25.0
arm_thickness = 3.0
arm_overlap = 5.0       # Amount the arm embeds into the head

# Tab dimensions (The blocks on the underside)
tab_length = 10.0
tab_width = 10.0
tab_height = 6.0
tab_start_offset = 20.0 # Distance from head to first tab
tab_spacing = 30.0      # Center-to-center spacing

# --- Geometry Construction ---

# 1. Create the Head
# The head has a lenticular (lens-shaped) profile on the XZ plane, extruded along Y.
# We create this by connecting four points with two 3-point arcs.
p_left = (-head_profile_len / 2.0, 0)
p_right = (head_profile_len / 2.0, 0)
p_top = (0, head_profile_ht / 2.0)
p_bottom = (0, -head_profile_ht / 2.0)

head = (
    cq.Workplane("XZ")
    .moveTo(*p_left)
    .threePointArc(p_top, p_right)      # Top arc
    .threePointArc(p_bottom, p_left)    # Bottom arc
    .close()
    .extrude(head_width / 2.0, both=True) # Extrude symmetrically in Y
)

# 2. Create the Arm
# A flat rectangular box extending along the +X axis.
# It is positioned to overlap the head slightly to ensure a solid union.
arm_center_x = (head_profile_len / 2.0) + (arm_length / 2.0) - arm_overlap

arm = (
    cq.Workplane("XY")
    .box(arm_length, arm_width, arm_thickness)
    .translate((arm_center_x, 0, 0))
)

# 3. Create the Tabs
# Two rectangular blocks on the bottom face of the arm (-Z direction).
tab_z_pos = -(arm_thickness / 2.0) - (tab_height / 2.0)
tab1_x_pos = (head_profile_len / 2.0) + tab_start_offset
tab2_x_pos = tab1_x_pos + tab_spacing

tab1 = (
    cq.Workplane("XY")
    .box(tab_length, tab_width, tab_height)
    .translate((tab1_x_pos, 0, tab_z_pos))
)

tab2 = (
    cq.Workplane("XY")
    .box(tab_length, tab_width, tab_height)
    .translate((tab2_x_pos, 0, tab_z_pos))
)

# 4. Combine all parts into the final result
result = head.union(arm).union(tab1).union(tab2)