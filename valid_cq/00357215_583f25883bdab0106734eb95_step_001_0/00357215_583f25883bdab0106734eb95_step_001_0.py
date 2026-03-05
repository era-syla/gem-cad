import cadquery as cq

# Parameters for the connecting rod
length = 100.0          # Distance between hole centers
boss_radius = 15.0      # Radius of the cylindrical ends
hole_radius = 8.0       # Radius of the mounting holes
thickness = 12.0        # Thickness of the material
arm_width = 20.0        # Width of the central connecting arm
z_offset = 15.0         # Vertical offset between the two ends

# 1. Create the Left Boss (at origin)
boss_left = (
    cq.Workplane("XY")
    .circle(boss_radius)
    .extrude(thickness)
)

# 2. Create the Right Boss (offset in X and Z)
boss_right = (
    cq.Workplane("XY")
    .workplane(offset=z_offset)
    .center(length, 0)
    .circle(boss_radius)
    .extrude(thickness)
)

# 3. Create the Connecting Arm
# Loft a rectangular profile from the left boss to the right boss.
# We define the cross-sections on the YZ plane (perpendicular to the length).
arm = (
    cq.Workplane("YZ")
    .center(0, thickness / 2.0)     # Align center with the middle of the left boss height
    .rect(arm_width, thickness)     # Profile at X=0
    .workplane(offset=length)       # Create a new plane at X=length
    .center(0, z_offset)            # Shift center vertically to match the right boss
    .rect(arm_width, thickness)     # Profile at X=length
    .loft(combine=True)             # Create solid connecting the profiles
)

# 4. Combine Bosses and Arm
solid_body = boss_left.union(boss_right).union(arm)

# 5. Cut the Holes
# Define cutters with enough length to pierce through
hole_cutter_left = (
    cq.Workplane("XY")
    .circle(hole_radius)
    .extrude(thickness * 3)
    .translate((0, 0, -thickness)) # Ensure cutter passes through bottom face
)

hole_cutter_right = (
    cq.Workplane("XY")
    .workplane(offset=z_offset)
    .center(length, 0)
    .circle(hole_radius)
    .extrude(thickness * 3)
    .translate((0, 0, -thickness))
)

# Apply the cuts
result = solid_body.cut(hole_cutter_left).cut(hole_cutter_right)