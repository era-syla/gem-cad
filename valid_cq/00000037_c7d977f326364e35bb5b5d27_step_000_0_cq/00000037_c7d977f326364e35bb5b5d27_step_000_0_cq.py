import cadquery as cq
import math

# --- Parameters ---

# Main Tail Boom / Tube
tube_od = 8.0
tube_id = 7.0
tube_length = 60.0

# Servo Motor (Generic cylinder representation)
servo_dia = 20.0
servo_height = 25.0
servo_shaft_dia = 4.0
servo_shaft_len = 15.0

# Linkage Arm (L-shaped)
arm_thickness = 4.0
arm_width = 8.0
arm_len_1 = 30.0  # Horizontal part
arm_len_2 = 25.0  # Vertical part towards tail hub

# Tail Rotor Hub / Gearbox Housing
hub_center_dia = 12.0
hub_thickness = 5.0
hub_shaft_dia = 3.0

# Tail Blade Grips (Simplified)
grip_dia = 6.0
grip_height = 8.0

# Support Bracket (C-shape clamp)
bracket_width = 10.0
bracket_height = 25.0
bracket_thickness = 3.0
bracket_hole_spacing = 18.0

# Slider mechanism
slider_dia = 10.0
slider_width = 10.0
linkage_ball_dia = 3.0

# --- Geometry Construction ---

# 1. Main Tube (Tail Boom)
# Created along X-axis
boom = (cq.Workplane("YZ")
        .circle(tube_od/2)
        .extrude(tube_length)
        .faces(">X").workplane()
        .hole(tube_id, tube_length)
        )

# 2. Servo Motor
# Positioned above the boom
servo = (cq.Workplane("XY")
         .circle(servo_dia/2)
         .extrude(servo_height)
         # Add shaft
         .faces(">Z").workplane()
         .circle(servo_shaft_dia/2)
         .extrude(servo_shaft_len)
         # Rotate and move to position
         .rotate((0,0,0), (0,1,0), 90)
         .translate((tube_length - 20, 25, 0))
         )

# 3. L-Shaped Control Arm / Bellcrank
# Connecting servo linkage to tail pitch slider
arm_path = (cq.Workplane("XY")
            .moveTo(0, 0)
            .lineTo(arm_len_1, 0)
            .lineTo(arm_len_1, -arm_len_2)
            )

# Create the profile and sweep or extrude
# Let's make it a simple union of rectangular solids for robustness
arm_part1 = (cq.Workplane("XY")
             .rect(arm_len_1 + arm_width, arm_width)
             .extrude(arm_thickness)
             )

arm_part2 = (cq.Workplane("XY")
             .rect(arm_width, arm_len_2)
             .extrude(arm_thickness)
             .translate((arm_len_1/2, -arm_len_2/2 + arm_width/2, 0))
             )

# Yoke/Fork at the end (connects to slider)
fork = (cq.Workplane("XZ")
        .rect(arm_thickness, 10)
        .extrude(8)
        .faces(">Y").workplane()
        .hole(3)
        .translate((arm_len_1/2, -arm_len_2, arm_thickness/2))
        )
        
control_arm = (arm_part1
               .union(arm_part2)
               .union(fork)
               .translate((tube_length - 40, 10, 0))
               )


# 4. Tail Rotor Gearbox Housing (The "Hub")
# Located at the end of the arm
hub = (cq.Workplane("YZ")
       .circle(hub_center_dia/2)
       .extrude(hub_thickness)
       )

# Vertical shafts for blade grips
hub_vertical = (cq.Workplane("XY")
                .circle(hub_shaft_dia/2)
                .extrude(20)
                .translate((0, 0, -10))
                )

# Add bolt pattern details to hub
bolt_circle = (cq.Workplane("YZ")
               .workplane(offset=hub_thickness)
               .polarArray(3, 0, 360, 6)
               .circle(0.8)
               .extrude(-1.0)
               )

tail_unit = (hub
             .union(hub_vertical)
             .cut(bolt_circle)
             .rotate((0,0,0), (0,0,1), -90)
             .translate((tube_length + 5, -arm_len_2 + 10, 0))
             )


# 5. Tail Pitch Slider (Sleeve on the shaft)
slider_sleeve = (cq.Workplane("YZ")
                 .circle(slider_dia/2)
                 .extrude(slider_width)
                 .faces(">X").workplane()
                 .hole(tube_od + 0.5) # Fits over a shaft usually inside the boom
                 )

slider_link_mount = (cq.Workplane("XY")
                     .rect(5, 5)
                     .extrude(8)
                     .translate((0, 0, slider_dia/2))
                     .rotate((0,0,0), (0,1,0), 90)
                     )

slider = (slider_sleeve
          .union(slider_link_mount)
          .translate((tube_length - 15, -arm_len_2 + 10, 0))
          )

# 6. Support Bracket (Far right in image)
bracket_profile = (cq.Workplane("YZ")
                   .moveTo(0, 0)
                   .lineTo(0, bracket_height)
                   .lineTo(bracket_thickness, bracket_height)
                   .lineTo(bracket_thickness, bracket_height - 5)
                   .lineTo(bracket_width, bracket_height/2 + 2)
                   .lineTo(bracket_width, bracket_height/2 - 2)
                   .lineTo(bracket_thickness, 5)
                   .lineTo(bracket_thickness, 0)
                   .close()
                   .extrude(5)
                   )

bracket_holes = (cq.Workplane("YZ")
                 .pushPoints([(bracket_thickness/2, 2.5), (bracket_thickness/2, bracket_height - 2.5)])
                 .circle(1.5)
                 .extrude(5)
                 )

bracket = (bracket_profile
           .cut(bracket_holes)
           .translate((tube_length + 15, -arm_len_2 + 5, -2.5))
           )

# 7. Pushrod Guide / Fin (attached to boom)
fin = (cq.Workplane("XY")
       .moveTo(0, 0)
       .lineTo(30, 0)
       .lineTo(30, 2)
       .lineTo(5, 5)
       .lineTo(0, 5)
       .close()
       .extrude(1.5)
       .rotate((0,0,0), (1,0,0), 90)
       .translate((10, 0, tube_od/2))
       )


# --- Assembly ---
result = (boom
          .union(servo)
          .union(control_arm)
          .union(tail_unit)
          .union(slider)
          .union(bracket)
          .union(fin)
          )

# Export or Render
if 'show_object' in globals():
    show_object(result)