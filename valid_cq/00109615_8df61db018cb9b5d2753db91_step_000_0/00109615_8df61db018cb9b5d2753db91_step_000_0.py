import cadquery as cq

# Parametric dimensions for the model
height = 80.0             # Total height of the vertical column
col_width = 30.0          # Width of the vertical column section
arm_length = 40.0         # Horizontal length of the extending arm
arm_tip_h = 18.0          # Height of the vertical face at the tip of the arm
arm_tip_y = 42.0          # Y-coordinate of the bottom of the arm tip
arm_join_y = 25.0         # Y-coordinate where the bottom of the arm meets the column
extrude_depth = 25.0      # Thickness of the part

# Calculate key vertices based on parameters
# (0,0) is at the bottom-left corner
p_bl = (0, 0)
p_tl = (0, height)
p_tr_col = (col_width, height - 5.0)  # Top edge slants slightly downwards

p_arm_tip_top = (col_width + arm_length, arm_tip_y + arm_tip_h)
p_arm_tip_bot = (col_width + arm_length, arm_tip_y)
p_arm_root = (col_width, arm_join_y)
p_br_col = (col_width, 0)

# Define a midpoint for the concave arc connecting the column to the arm
# This creates the "scoop" shape seen in the image
arc_mid_x = col_width + (arm_length * 0.25)
arc_mid_y = height - 22.0
p_arc_mid = (arc_mid_x, arc_mid_y)

# Generate the geometry
result = (
    cq.Workplane("XY")
    .moveTo(*p_bl)
    .lineTo(*p_tl)
    .lineTo(*p_tr_col)
    # Concave arc connecting the top column to the arm tip
    .threePointArc(p_arc_mid, p_arm_tip_top)
    .lineTo(*p_arm_tip_bot)
    # Slanted bottom of the arm
    .lineTo(*p_arm_root)
    .lineTo(*p_br_col)
    .close()
    .extrude(extrude_depth)
)

# Optional: Generate the small chip artifact seen in the distance
# (Included to match the image content, though likely a secondary detail)
small_chip = (
    cq.Workplane("XY")
    .rect(12, 12)
    .extrude(3)
    .edges("|Z").fillet(3)
    .translate((-40, -40, 0))
)

# Combine the main part with the small chip
result = result.union(small_chip)