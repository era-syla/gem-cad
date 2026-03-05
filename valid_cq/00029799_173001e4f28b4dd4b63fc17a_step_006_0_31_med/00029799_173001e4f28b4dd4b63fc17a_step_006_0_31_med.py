import cadquery as cq

# Parametric dimensions
arm_width = 16.0
arm_length = 35.0
arm_thickness = 10.0
hole_radius = 3.5

side_peg_radius = 3.5
side_peg_length = 15.0
side_peg_y_offset = 15.0

cap_radius = 10.0
cap_thickness = 8.0
cap_pin_radius = 1.5
cap_pin_length = 6.0
cap_pin_spacing = 4.0

small_pin_radius = 2.0
small_pin_length = 12.0

# 1. Main Arm with rounded end and hole
arm = (cq.Workplane("XY")
       .moveTo(-arm_width / 2, 0)
       .lineTo(-arm_width / 2, arm_length)
       .tangentArcPoint((arm_width / 2, arm_length))
       .lineTo(arm_width / 2, 0)
       .close()
       .extrude(arm_thickness))

# Add through hole in the rounded end
arm = arm.faces(">Z").workplane().center(0, arm_length).hole(hole_radius * 2)

# Add side peg to the arm
peg = cq.Workplane("YZ").circle(side_peg_radius).extrude(side_peg_length)
peg = peg.translate((arm_width / 2, side_peg_y_offset, arm_thickness / 2))
arm = arm.union(peg)

# 2. Cap with two pins
cap_body = cq.Workplane("YZ").circle(cap_radius).extrude(cap_thickness)
cap_pins = (cq.Workplane("YZ")
            .pushPoints([(cap_pin_spacing, 0), (-cap_pin_spacing, 0)])
            .circle(cap_pin_radius)
            .extrude(-cap_pin_length))

# Position the cap to the side of the arm
cap = cap_body.union(cap_pins).translate((arm_width + 20, arm_length, arm_thickness / 2))

# 3. Three standalone small pins arranged diagonally
pins = (cq.Workplane("XY")
        .workplane(offset=-25)
        .pushPoints([(15, -5), (25, -15), (35, -25)])
        .circle(small_pin_radius)
        .extrude(small_pin_length))

# Combine all components into the final result
result = cq.Workplane("XY").add(arm).add(cap).add(pins)