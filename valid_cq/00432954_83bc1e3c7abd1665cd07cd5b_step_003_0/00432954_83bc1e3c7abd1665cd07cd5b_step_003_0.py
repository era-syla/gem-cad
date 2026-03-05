import cadquery as cq

# --- Parameters ---
# Overall dimensions
base_length = 120.0
base_width = 60.0
plate_thickness = 6.0
gap_height = 24.0
total_base_height = plate_thickness * 2 + gap_height

# Column dimensions
col_width = 40.0
col_height = 300.0
col_wall = 3.0

# Motor dimensions
motor_dia = 54.0
motor_height = 90.0
motor_cap_dia = 32.0
motor_cap_height = 5.0

# Positioning
col_center_x = -base_length/2 + col_width/2 + 10
motor_center_x = col_center_x + col_width/2 + 10 + motor_dia/2

# --- Base Assembly ---
# Bottom Plate
bottom_plate = cq.Workplane("XY").box(base_length, base_width, plate_thickness)

# Top Plate
top_plate = (cq.Workplane("XY")
             .workplane(offset=plate_thickness + gap_height)
             .box(base_length, base_width, plate_thickness))

# Slot in Top Plate (under motor area)
slot_cut = (cq.Workplane("XY")
            .workplane(offset=plate_thickness + gap_height)
            .center(motor_center_x, 0)
            .slot2D(motor_dia - 15, 8)
            .extrude(plate_thickness))
top_plate = top_plate.cut(slot_cut)

# Base Spacers - Column Side (Split to allow visibility of internals)
spacer_left = (cq.Workplane("XY")
               .workplane(offset=plate_thickness)
               .center(col_center_x, base_width/2 - 6)
               .box(col_width + 10, 12, gap_height))
spacer_right = (cq.Workplane("XY")
                .workplane(offset=plate_thickness)
                .center(col_center_x, -base_width/2 + 6)
                .box(col_width + 10, 12, gap_height))

# Base Spacers - Motor Side (Pillars)
spacer_pillars = (cq.Workplane("XY")
                  .workplane(offset=plate_thickness)
                  .rect(base_length - 12, base_width - 12, forConstruction=True)
                  .vertices(">X") # Select vertices on the right side
                  .circle(5)
                  .extrude(gap_height))

# Base Bolts (Hex heads on top)
base_bolts = (cq.Workplane("XY")
              .workplane(offset=total_base_height)
              .rect(base_length - 12, base_width - 12, forConstruction=True)
              .vertices()
              .polygon(6, 7) # Hexagon radius
              .extrude(4))

# Internal Coupling/Pulley
coupling = (cq.Workplane("XY")
            .workplane(offset=plate_thickness + 2)
            .center(col_center_x, 0)
            .circle(16)
            .extrude(gap_height - 4))

base_assembly = bottom_plate.union(top_plate).union(spacer_left).union(spacer_right).union(spacer_pillars).union(base_bolts).union(coupling)

# --- Linear Actuator Column ---
# Main Tube
column = (cq.Workplane("XY")
          .workplane(offset=total_base_height)
          .center(col_center_x, 0)
          .rect(col_width, col_width)
          .extrude(col_height))

# Top Cap
col_cap = (cq.Workplane("XY")
           .workplane(offset=total_base_height + col_height)
           .center(col_center_x, 0)
           .rect(col_width, col_width)
           .extrude(6))

# Output Shaft/Interface
shaft_height = 18
shaft = (cq.Workplane("XY")
         .workplane(offset=total_base_height + col_height + 6)
         .center(col_center_x, 0)
         .circle(12)
         .extrude(shaft_height))

# Hollow shaft and pin hole
shaft_bore = (cq.Workplane("XY")
              .workplane(offset=total_base_height + col_height + 6)
              .center(col_center_x, 0)
              .circle(9)
              .extrude(shaft_height))

shaft_pin_hole = (cq.Workplane("XZ")
                  .workplane(offset=-col_center_x) # Center Y plane relative to column
                  .center(0, total_base_height + col_height + 6 + shaft_height/2)
                  .circle(2.5)
                  .extrude(30, both=True))

shaft = shaft.cut(shaft_bore).cut(shaft_pin_hole)

# Cap Bolts
cap_bolts = (cq.Workplane("XY")
             .workplane(offset=total_base_height + col_height + 6)
             .center(col_center_x, 0)
             .rect(col_width - 10, col_width - 10, forConstruction=True)
             .vertices()
             .circle(2)
             .extrude(2))

column_assembly = column.union(col_cap).union(shaft).union(cap_bolts)

# --- Motor ---
motor_body = (cq.Workplane("XY")
              .workplane(offset=total_base_height)
              .center(motor_center_x, 0)
              .circle(motor_dia/2)
              .extrude(motor_height))

motor_top_detail = (cq.Workplane("XY")
                    .workplane(offset=total_base_height + motor_height)
                    .center(motor_center_x, 0)
                    .circle(motor_cap_dia/2)
                    .extrude(motor_cap_height))

motor_encoder_nub = (cq.Workplane("XY")
                     .workplane(offset=total_base_height + motor_height + motor_cap_height)
                     .center(motor_center_x + 8, 0)
                     .circle(3)
                     .extrude(3))

motor_bolts = (cq.Workplane("XY")
               .workplane(offset=total_base_height)
               .center(motor_center_x, 0)
               .rect(motor_dia + 10, motor_dia + 10, forConstruction=True)
               .vertices()
               .circle(2.5)
               .extrude(4))

motor_assembly = motor_body.union(motor_top_detail).union(motor_encoder_nub).union(motor_bolts)

# --- Mounting Bracket ---
# L-bracket attached to the front face of the column
brack_z_pos = total_base_height + 30
brack_width = 20
brack_thick = 4
brack_len = 25

# Profile created on YZ plane, extruded along X
# Coordinates relative to the center of the column face
brack_profile = (cq.Workplane("YZ")
                 .workplane(offset=col_center_x - brack_width/2)
                 .moveTo(-col_width/2, brack_z_pos) # Point on column face
                 .lineTo(-col_width/2, brack_z_pos + brack_len) # Vertical Up
                 .lineTo(-col_width/2 - brack_thick, brack_z_pos + brack_len) # Thickness
                 .lineTo(-col_width/2 - brack_thick, brack_z_pos + brack_thick) # Inner Corner
                 .lineTo(-col_width/2 - brack_len, brack_z_pos + brack_thick) # Horizontal Out
                 .lineTo(-col_width/2 - brack_len, brack_z_pos) # Thickness Down
                 .close()
                 .extrude(brack_width))

# Hole in the horizontal leg of the bracket
brack_hole = (cq.Workplane("XY")
              .workplane(offset=brack_z_pos + brack_thick/2)
              .center(col_center_x, -col_width/2 - brack_len/2 - 2)
              .circle(3.5)
              .extrude(10))

bracket_final = brack_profile.cut(brack_hole)

# --- Final Assembly ---
result = base_assembly.union(column_assembly).union(motor_assembly).union(bracket_final)