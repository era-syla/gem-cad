import cadquery as cq

# Parametric dimensions based on the visual proportions
base_diameter = 40.0
base_thickness = 5.0
boss_diameter = 25.0
boss_height = 3.0
arm_width = 8.0
arm_length = 50.0   # Distance from center of disc to tip of arm
arm_thickness = 5.0 # Matches base thickness

# Derived dimensions
base_radius = base_diameter / 2.0
boss_radius = boss_diameter / 2.0
arm_radius = arm_width / 2.0
arm_straight_len = arm_length - arm_radius

# 1. Create the Base Disc
# We start on the XY plane and extrude upwards
base = cq.Workplane("XY").circle(base_radius).extrude(base_thickness)

# 2. Create the Central Boss
# Select the top face of the base and extrude the boss cylinder
# This automatically fuses the boss to the base
main_body = (
    base.faces(">Z")
    .workplane()
    .circle(boss_radius)
    .extrude(boss_height)
)

# 3. Create the Extending Arm
# We create a sketch for the arm profile on the XY plane.
# The profile starts at x=0 (center of disc) to ensure a solid overlap/connection.
# The tip is a semi-circle.
arm_sketch = (
    cq.Workplane("XY")
    .moveTo(0, -arm_radius)                       # Start at bottom-left corner (at center)
    .lineTo(arm_straight_len, -arm_radius)        # Line to start of the arc
    .threePointArc(
        (arm_length, 0),                          # Midpoint of arc (the tip)
        (arm_straight_len, arm_radius)            # End point of arc
    )
    .lineTo(0, arm_radius)                        # Line back to top-left corner
    .close()
)

arm = arm_sketch.extrude(arm_thickness)

# 4. Combine the Arm with the Main Body
result = main_body.union(arm)