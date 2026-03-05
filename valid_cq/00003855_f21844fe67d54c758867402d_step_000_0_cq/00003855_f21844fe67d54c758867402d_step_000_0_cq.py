import cadquery as cq

# --- Parametric Dimensions ---
# Main Arm
arm_length = 100.0
arm_width = 8.0
arm_height = 4.0
arm_fillet_radius = 1.0 # Slight rounding on the arm edges

# Fork End (Left side)
fork_length = 25.0
fork_height = 20.0
fork_thickness = 4.0
fork_gap = 6.0
fork_chamfer = 8.0 # Diagonal cut on the top corner

# Boss/Cylinder End (Right side)
boss_height = 15.0
boss_diameter_outer = 10.0
boss_diameter_inner = 6.0
boss_flange_diameter = 12.0
boss_flange_height = 2.0
hex_socket_size = 3.0 # Radius (or apothem) of hexagon
hex_socket_depth = 5.0

# --- Modeling ---

# 1. Create the Main Arm
# We start with a simple rectangular bar.
arm = (
    cq.Workplane("XY")
    .box(arm_length, arm_width, arm_height)
    .translate((arm_length / 2, 0, arm_height / 2))
)

# 2. Create the Fork End
# The fork consists of two vertical plates separated by a gap.
# We will create one plate, mirror it, and cut the gap, or build two blocks.
# Let's build a solid block at the end and cut the slot.

fork_block_width = fork_thickness * 2 + fork_gap
fork_center_offset = (arm_length - fork_length / 2) # Position at the very end

# Create the bulk material for the fork
fork_block = (
    cq.Workplane("XY")
    .box(fork_length, fork_block_width, fork_height)
    .translate((fork_length / 2, 0, fork_height / 2))
)

# Create the slot cutout
slot_cutout = (
    cq.Workplane("XY")
    .box(fork_length, fork_gap, fork_height)
    .translate((fork_length / 2, 0, fork_height / 2))
)

# Create the chamfer profile on the fork
# We want to slice off the top-inner corner of the fork ears.
# Instead of a complex chamfer op, let's just make a cutting shape.
chamfer_cut = (
    cq.Workplane("XZ")
    .moveTo(fork_length, fork_height)
    .lineTo(fork_length - fork_chamfer, fork_height)
    .lineTo(fork_length, fork_height - fork_chamfer)
    .close()
    .extrude(fork_block_width / 2 + 1, both=True) # Extrude enough to cut both ears
)

# Combine fork elements
fork = fork_block.cut(slot_cutout).cut(chamfer_cut)

# 3. Create the Cylindrical Boss End
# Positioned at the opposite end of the arm (x = arm_length)

boss_pos_x = arm_length
boss_pos_z = 0 # Base at ground level

# Main cylinder body
boss_main = (
    cq.Workplane("XY")
    .circle(boss_diameter_outer / 2)
    .extrude(boss_height)
    .translate((boss_pos_x, 0, 0))
)

# Top flange (rim)
boss_flange = (
    cq.Workplane("XY")
    .workplane(offset=boss_height - boss_flange_height)
    .circle(boss_flange_diameter / 2)
    .extrude(boss_flange_height)
    .translate((boss_pos_x, 0, 0))
)

# Combine boss parts
boss = boss_main.union(boss_flange)

# Hex hole
hex_cut = (
    cq.Workplane("XY")
    .workplane(offset=boss_height - hex_socket_depth)
    .polygon(6, hex_socket_size * 2) # 6 sides, diameter approx 2*size
    .extrude(hex_socket_depth)
    .translate((boss_pos_x, 0, 0))
)

# Through hole (circular)
through_hole = (
    cq.Workplane("XY")
    .circle(boss_diameter_inner / 2)
    .extrude(boss_height)
    .translate((boss_pos_x, 0, 0))
)

# Apply cuts to boss
boss = boss.cut(hex_cut).cut(through_hole)


# 4. Assembly and Refinement

# Union the main parts
result = arm.union(fork).union(boss)

# Add triangular reinforcement rib at the boss connection
rib_length = 15.0
rib_height = 8.0
rib_thickness = 2.0

rib = (
    cq.Workplane("XZ")
    .moveTo(boss_pos_x - boss_diameter_outer/2, arm_height)
    .lineTo(boss_pos_x - boss_diameter_outer/2 - rib_length, arm_height)
    .lineTo(boss_pos_x - boss_diameter_outer/2, arm_height + rib_height)
    .close()
    .extrude(rib_thickness/2, both=True)
)

result = result.union(rib)

# Add reinforcement/transition at the fork connection
# A simple chamfer or fillet or small wedge where the arm meets the fork plate
# looking at the image, the arm seems to just merge into the fork base.
# The fork is wider than the arm.

# Optional: Add fillets to smooth transitions
# Fillet the long edges of the arm for that "molded" look
try:
    result = result.edges(f"|X and >Y and <Z[{arm_height}]").fillet(0.5)
    result = result.edges(f"|X and <Y and <Z[{arm_height}]").fillet(0.5)
except:
    pass # Skip if topology is too complex for simple selection

# Final Result
result = result