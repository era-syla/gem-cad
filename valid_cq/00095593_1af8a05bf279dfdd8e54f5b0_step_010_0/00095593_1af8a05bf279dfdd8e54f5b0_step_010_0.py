import cadquery as cq

# ==========================================
# Parameter Definitions
# ==========================================

# Main Housing Body
main_height = 60.0
main_width = 40.0   # Dimension along Y
main_thick = 15.0   # Dimension along X

# Base Plate
base_height = 5.0
base_width = 50.0   # Slightly wider than the main housing
base_overhang = 20.0 # Extension length towards the front (-X)

# Rear Arms (Rails)
arm_length = 90.0
arm_width = 30.0    # Narrower than main housing
arm_height = 12.0
arm_gap = 25.0      # Vertical spacing between arms

# Front Assembly
leg_height = 10.0
leg_thick = 5.0
front_plate_thick = 3.0

# ==========================================
# Geometry Construction
# ==========================================

# 1. Main Housing Block
# Positioned on top of the base plate.
# Back face aligned with X=0.
housing = (cq.Workplane("XY")
           .workplane(offset=base_height)
           .center(-main_thick / 2, 0)
           .box(main_thick, main_width, main_height, centered=(True, True, False))
           )

# 2. Base Plate
# Positioned at Z=0.
# Extends from X=0 (back) to X=-(main_thick + base_overhang) (front).
total_base_len = main_thick + base_overhang
base = (cq.Workplane("XY")
        .center(-total_base_len / 2, 0)
        .box(total_base_len, base_width, base_height, centered=(True, True, False))
        )

# 3. Rear Arms
# Extruding from the back face (X=0 plane) in +X direction.

# Top Arm: Aligned with the top of the housing
top_arm_z_center = base_height + main_height - arm_height / 2
top_arm = (cq.Workplane("YZ")
           .workplane(offset=0)
           .center(0, top_arm_z_center)
           .rect(arm_width, arm_height)
           .extrude(arm_length)
           )

# Bottom Arm: Spaced below the top arm
bot_arm_z_center = top_arm_z_center - arm_height - arm_gap
bot_arm = (cq.Workplane("YZ")
           .workplane(offset=0)
           .center(0, bot_arm_z_center)
           .rect(arm_width, arm_height)
           .extrude(arm_length)
           )

# Feature: Undercut/Notch at the tip of the arms (bottom side)
notch_len = 8.0
notch_depth = 4.0

# Create cutting tool for the notch
notch_tool_top = (cq.Workplane("XY")
                  .workplane(offset=top_arm_z_center - arm_height / 2)
                  .center(arm_length - notch_len / 2, 0)
                  .box(notch_len, arm_width + 1.0, notch_depth * 2, centered=(True, True, True))
                  )

notch_tool_bot = (cq.Workplane("XY")
                  .workplane(offset=bot_arm_z_center - arm_height / 2)
                  .center(arm_length - notch_len / 2, 0)
                  .box(notch_len, arm_width + 1.0, notch_depth * 2, centered=(True, True, True))
                  )

# Apply cuts
top_arm = top_arm.cut(notch_tool_top)
bot_arm = bot_arm.cut(notch_tool_bot)

# 4. Front Legs / Undercarriage
# Located under the overhang section of the base plate (Negative Z)
# X range: Covers the overhang area
leg_x_center = -(main_thick + base_overhang / 2)
leg_y_offset = base_width / 2 - leg_thick / 2

# Left Leg
left_leg = (cq.Workplane("XY")
            .workplane(offset=-leg_height)
            .center(leg_x_center, leg_y_offset)
            .box(base_overhang, leg_thick, leg_height, centered=(True, True, False))
            )

# Right Leg
right_leg = (cq.Workplane("XY")
             .workplane(offset=-leg_height)
             .center(leg_x_center, -leg_y_offset)
             .box(base_overhang, leg_thick, leg_height, centered=(True, True, False))
             )

# Front Bumper/Cap
# A small vertical plate at the very front of the legs
front_cap = (cq.Workplane("YZ")
             .workplane(offset=-(total_base_len + front_plate_thick))
             .center(0, -leg_height / 2)
             .rect(base_width, leg_height)
             .extrude(front_plate_thick)
             )

# ==========================================
# Assembly
# ==========================================

result = (housing
          .union(base)
          .union(top_arm)
          .union(bot_arm)
          .union(left_leg)
          .union(right_leg)
          .union(front_cap)
          )