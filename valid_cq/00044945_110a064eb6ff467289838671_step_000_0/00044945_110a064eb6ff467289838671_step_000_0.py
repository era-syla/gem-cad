import cadquery as cq

# --- Parametric Dimensions ---
motor_diam = 36.0
motor_length = 65.0
housing_w = 46.0
housing_d = 50.0
housing_h = 70.0
arm_diam = 12.0
arm_length = 90.0
arm_z_pos = 45.0  # Vertical position of the arm axis relative to motor base
end_block_size = 26.0

# --- 1. Motor Unit (Bottom) ---
motor = (cq.Workplane("XY")
         .circle(motor_diam / 2)
         .extrude(-motor_length)
         # Chamfer bottom edge for realism
         .edges("<Z").chamfer(1.0)
         )

# Motor bottom bearing boss
motor_boss = (cq.Workplane("XY")
              .workplane(offset=-motor_length)
              .circle(6)
              .extrude(-4)
              )

# --- 2. Main Gearbox Housing (Middle) ---
# Base Flange connecting to motor
base = (cq.Workplane("XY")
        .rect(housing_w, housing_d)
        .extrude(12)
        .edges("|Z").fillet(4)
        )

# Main Tower Body
tower = (cq.Workplane("XY")
         .workplane(offset=12)
         .rect(housing_w - 4, housing_d - 4)
         .extrude(housing_h - 12)
         .edges("|Z").fillet(5)
         )

# Top Cover with Ribs/Detail
# Create a cap block
top_cap = (cq.Workplane("XY")
           .workplane(offset=housing_h)
           .rect(housing_w, housing_d)
           .extrude(8)
           .edges().fillet(2)
           )

# Top Cylindrical Boss (Gear shaft housing)
top_boss = (cq.Workplane("XY")
            .workplane(offset=housing_h + 8)
            .center(5, 5)
            .circle(9)
            .extrude(6)
            .faces(">Z").workplane()
            .hole(4, 3) # Screw hole
            )

# Structural Ribs on top surface (Simplified)
ribs = (cq.Workplane("XY")
        .workplane(offset=housing_h + 8)
        .center(-8, -8)
        .rarray(6, 1, 3, 1) # Array of 3 ribs
        .rect(1.5, 12)
        .extrude(3)
        )

# --- 3. Electrical Connector (Side) ---
# Located on the -Y face (Front relative to typical orientation)
connector = (cq.Workplane("XZ")
             .workplane(offset=-housing_d / 2)
             .center(0, 20)  # Centered on X, Up 20 on Z
             .rect(24, 32)
             .extrude(-16)  # Extrude outwards
             .edges("|Y").fillet(2)
             )

# Connector inner detail
connector_plug = (cq.Workplane("XZ")
                  .workplane(offset=-housing_d / 2 - 16)
                  .center(0, 18)
                  .rect(18, 22)
                  .extrude(-6)
                  )

# --- 4. Actuator Arm (Extending Left) ---
# Output Hub on the -X face
arm_hub = (cq.Workplane("YZ")
           .workplane(offset=-housing_w / 2 + 2)
           .center(0, arm_z_pos)
           .circle(13)
           .extrude(-10)
           )

# The Extension Rod
arm = (cq.Workplane("YZ")
       .workplane(offset=-housing_w / 2 - 8)
       .center(0, arm_z_pos)
       .circle(arm_diam / 2)
       .extrude(-arm_length)
       )

# --- 5. End Effector (Tip) ---
# Block at the end of the rod
end_pos_x = -housing_w / 2 - 8 - arm_length

end_effector = (cq.Workplane("YZ")
                .workplane(offset=end_pos_x)
                .center(0, arm_z_pos)
                .rect(end_block_size, end_block_size)
                .extrude(-end_block_size)
                .edges().fillet(3)
                )

# Pivot/Mounting Boss on the End Effector
# Oriented vertically based on the image detail (cylinder sticking out)
end_pivot = (cq.Workplane("XY")
             .workplane(offset=arm_z_pos) # Center plane of arm
             .center(end_pos_x - end_block_size/2, 0) # Center of the block
             .circle(9)
             .extrude(end_block_size/2 + 4) # Extrude up
             .faces(">Z").workplane()
             .circle(5).extrude(3) # Small pin on top
             )

# Mirror pivot to bottom for symmetry (optional, but looks like a clevis or joint)
end_pivot_bottom = (cq.Workplane("XY")
             .workplane(offset=arm_z_pos)
             .center(end_pos_x - end_block_size/2, 0)
             .circle(9)
             .extrude(-(end_block_size/2 + 4))
             )

# --- Assembly ---
result = (motor
          .union(motor_boss)
          .union(base)
          .union(tower)
          .union(top_cap)
          .union(top_boss)
          .union(ribs)
          .union(connector)
          .union(connector_plug)
          .union(arm_hub)
          .union(arm)
          .union(end_effector)
          .union(end_pivot)
          .union(end_pivot_bottom)
          )

# Optional: Add mounting holes to the housing base for more detail
mounting_holes = (cq.Workplane("XY")
                  .workplane(offset=0)
                  .rect(housing_w + 10, housing_d + 10) # Wider than base
                  .rarray(housing_w + 4, housing_d, 2, 2)
                  .circle(2.5)
                  .extrude(12)
                  )
# We won't cut this since the base flange isn't wide enough in this simplified logic, 
# but this structure is how you would add them.
