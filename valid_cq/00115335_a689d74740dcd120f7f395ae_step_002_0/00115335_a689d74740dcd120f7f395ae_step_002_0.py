import cadquery as cq

# -- Parametric Dimensions --
arm_length = 55.0      # Length from center to the tip of an arm
arm_width = 16.0       # Outer width of the arm channel
arm_height = 18.0      # Overall height of the part
wall_thickness = 2.0   # Thickness of the walls and floor
boss_outer_dia = 8.0   # Outer diameter of the central cylindrical boss
boss_inner_dia = 4.0   # Inner diameter of the mounting hole

# -- Construction --

# 1. Create the base solid structure (Y-shape)
# We create a box for one arm. We extend the length backwards by 'arm_width'
# to ensure that when rotated, the arms overlap fully at the center hub.
box_len = arm_length + arm_width
arm_solid = (
    cq.Workplane("XY")
    .box(box_len, arm_width, arm_height)
    # Move the box so the 'back' end sits past the origin to cover the center
    .translate(((box_len / 2.0) - arm_width, 0, arm_height / 2.0))
)

# Create 3 arms rotated by 120 degrees and fuse them
arms = [arm_solid.rotate((0, 0, 0), (0, 0, 1), angle) for angle in [0, 120, 240]]
base_y_solid = arms[0].union(arms[1]).union(arms[2])

# 2. Create the hollow channel (Shelling)
# We select the top face (max Z) and shell inwards (negative thickness)
# This removes the top face and leaves walls/floor of the specified thickness.
shelled_body = base_y_solid.faces(">Z").shell(-wall_thickness)

# 3. Create the central boss
# A solid cylinder at the center, flush with the top height
center_boss = (
    cq.Workplane("XY")
    .circle(boss_outer_dia / 2.0)
    .extrude(arm_height)
)

# 4. Final Assembly
# Union the shelled body with the center boss, then cut the hole
result = (
    shelled_body
    .union(center_boss)
    .faces(">Z")           # Select the top face to define the hole location
    .workplane()
    .hole(boss_inner_dia)  # Cut a counterbored or simple hole (simple by default)
)