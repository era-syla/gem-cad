import cadquery as cq

# ---------------------------------------------------------
# Parametric Dimensions
# ---------------------------------------------------------
# Main Motor Body
motor_diameter = 32.0
motor_length = 50.0
crimp_offset = 2.5
crimp_width = 1.0
crimp_thickness = 0.5
body_chamfer = 0.5

# Rear Features (End Cap)
boss_rear_diam = 13.0
boss_rear_height = 3.0
term_diam = 2.6
term_height = 3.5
term_spacing = 8.0
term_offset_y = -10.0

# Front Features (Shaft End)
boss_front_diam = 10.0
boss_front_height = 1.5
shaft_diam = 3.175
shaft_length = 15.0
shaft_flat_depth = 0.5
shaft_flat_length = 12.0

# ---------------------------------------------------------
# 3D Modeling Logic
# ---------------------------------------------------------

# 1. Main Body Cylinder
# Oriented along Z-axis. Z=0 is the rear face.
main_body = cq.Workplane("XY").circle(motor_diameter / 2).extrude(motor_length)

# Add chamfers to the ends of the main body for a realistic look
main_body = main_body.edges("not |Z").chamfer(body_chamfer)

# 2. Crimp Ring Detail (Near Rear)
# Small ring protruding slightly to simulate the metal casing crimp
crimp_ring = (
    cq.Workplane("XY")
    .workplane(offset=crimp_offset)
    .circle((motor_diameter / 2) + crimp_thickness)
    .extrude(crimp_width)
)
main_body = main_body.union(crimp_ring)

# 3. Rear Boss (Bearing Housing)
# Extrudes outwards (Negative Z) from the rear face
rear_boss = (
    cq.Workplane("XY")
    .circle(boss_rear_diam / 2)
    .extrude(-boss_rear_height)
)
# Add a small chamfer to the boss edge
rear_boss = rear_boss.edges("<Z").chamfer(0.3)
main_body = main_body.union(rear_boss)

# 4. Rear Terminals
# Two small contacts positioned below the central axis
terminals = (
    cq.Workplane("XY")
    .pushPoints([
        (-term_spacing / 2, term_offset_y),
        (term_spacing / 2, term_offset_y)
    ])
    .circle(term_diam / 2)
    .extrude(-term_height)
)
# Round the tips of the terminals
terminals = terminals.edges("<Z").fillet((term_diam / 2) - 0.1)
main_body = main_body.union(terminals)

# 5. Front Boss
# Located on the front face (Z = motor_length)
front_boss = (
    cq.Workplane("XY")
    .workplane(offset=motor_length)
    .circle(boss_front_diam / 2)
    .extrude(boss_front_height)
)
main_body = main_body.union(front_boss)

# 6. Output Shaft
# Extends from the front boss
shaft_start_z = motor_length + boss_front_height
shaft = (
    cq.Workplane("XY")
    .workplane(offset=shaft_start_z)
    .circle(shaft_diam / 2)
    .extrude(shaft_length)
)

# 7. D-Cut (Flat section on shaft)
# Calculate the position for the cut based on depth
cut_dist_from_center = (shaft_diam / 2) - shaft_flat_depth
cut_tool_size = shaft_diam * 2  # Size of the cutting volume

# Create the cut from the tip of the shaft downwards
shaft_cut = (
    shaft.faces(">Z").workplane()
    # Center the cutting rectangle so its edge aligns with the cut depth
    .center(0, cut_dist_from_center + (cut_tool_size / 2))
    .rect(cut_tool_size, cut_tool_size)
    .cutBlind(-shaft_flat_length)
)

# Combine Shaft with Body
result = main_body.union(shaft_cut)