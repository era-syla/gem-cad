import cadquery as cq

# --- Parameters ---
# Dimensions estimated from the image
arm_length = 90.0
arm_width = 35.0
arm_thickness = 12.0

head_width = 110.0
head_depth = 25.0
head_thickness = 12.0

# The trapezoidal reinforcement boss under the head
boss_height = 12.0      # Extension downwards
boss_top_width = 55.0   # Width at the junction with the plate
boss_bot_width = 35.0   # Width at the bottom of the taper

hole_diameter = 8.0
hole_spacing = 80.0     # Distance between hole centers

# --- Geometry Construction ---

# 1. Create the Main Arm
# Aligned along negative X-axis, centered on Y, top face at Z=0
arm = (
    cq.Workplane("XY")
    .box(arm_length, arm_width, arm_thickness, centered=(False, True, False))
    .translate((-arm_length, 0, -arm_thickness))
)

# 2. Create the Head (Top Cross-bar)
# Aligned along positive X-axis (from origin), centered on Y, top face at Z=0
head_plate = (
    cq.Workplane("XY")
    .box(head_depth, head_width, head_thickness, centered=(False, True, False))
    .translate((0, 0, -head_thickness))
)

# 3. Create the Tapered Boss (Underneath the Head)
# Defined by a trapezoidal profile on the YZ plane (at X=0), extruded along X
boss_profile = [
    (boss_top_width / 2.0, -head_thickness),
    (boss_bot_width / 2.0, -(head_thickness + boss_height)),
    (-boss_bot_width / 2.0, -(head_thickness + boss_height)),
    (-boss_top_width / 2.0, -head_thickness)
]

boss = (
    cq.Workplane("YZ")
    .workplane(offset=0)
    .polyline(boss_profile)
    .close()
    .extrude(head_depth)
)

# 4. Combine Solids
base_geo = arm.union(head_plate).union(boss)

# 5. Add Mounting Holes
# Select the top face (Z=0), position points, and cut holes
result = (
    base_geo
    .faces(">Z")
    .workplane()
    .pushPoints([
        (head_depth / 2.0, -hole_spacing / 2.0),
        (head_depth / 2.0, hole_spacing / 2.0)
    ])
    .hole(hole_diameter)
)