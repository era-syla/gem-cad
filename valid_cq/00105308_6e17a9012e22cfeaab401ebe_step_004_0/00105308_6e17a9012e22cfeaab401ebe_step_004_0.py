import cadquery as cq

# --- Parametric Dimensions ---
# Fork (Clevis) geometry settings
num_prongs = 3
prong_thickness = 3.5      # Width of each prong
gap_thickness = 3.5        # Spacing between prongs
fork_depth = 14.0          # Depth of the part (Y-axis dimension)
base_thickness = 5.0       # Thickness of the solid base plate connecting prongs
hole_center_height = 12.0  # Distance from the top of the base to the hole center
hole_diameter = 5.0        # Diameter of the through-hole

# Shaft geometry settings
shaft_diameter = 8.0
shaft_length = 30.0

# --- Derived Calculations ---
# Calculate total width based on prongs and gaps
total_width = (num_prongs * prong_thickness) + ((num_prongs - 1) * gap_thickness)
# Calculate fillet radius for a fully rounded top (half of depth)
fillet_radius = fork_depth / 2.0
# Total height of the upper fork section
total_fork_height = base_thickness + hole_center_height + fillet_radius

# --- Modeling Process ---

# 1. Create the main block for the fork
# Centered on X and Y, base sits on Z=0
fork_block = (
    cq.Workplane("XY")
    .box(total_width, fork_depth, total_fork_height, centered=(True, True, False))
)

# 2. Fillet the top edges to create the rounded profile
# We select edges parallel to the X-axis located at the top (highest Z)
# Subtracting a tiny epsilon from radius prevents topological singularities
fork_rounded = (
    fork_block
    .edges("|X and >Z")
    .fillet(fillet_radius - 0.01)
)

# 3. Create the through-hole
# The hole runs along the X-axis at the calculated height
hole_z_pos = base_thickness + hole_center_height
hole_cutter = (
    cq.Workplane("YZ")
    .circle(hole_diameter / 2.0)
    .extrude(total_width * 2, both=True)
    .translate((0, 0, hole_z_pos))
)

fork_with_hole = fork_rounded.cut(hole_cutter)

# 4. Cut the slots to form the prongs
# Calculate the center X position for each gap
start_x = -total_width / 2.0
gap_centers = []
# The center of the first gap is: Start + Prong Width + Half Gap Width
current_gap_x = start_x + prong_thickness + (gap_thickness / 2.0)

for _ in range(num_prongs - 1):
    gap_centers.append(current_gap_x)
    current_gap_x += (prong_thickness + gap_thickness)

fork_slotted = fork_with_hole
for gap_x in gap_centers:
    # Create a cutter block for the gap
    # Width = gap_thickness, Depth > part depth, Height from base to top
    slot_cutter = (
        cq.Workplane("XY")
        .box(gap_thickness, fork_depth * 2, total_fork_height, centered=(True, True, False))
        .translate((gap_x, 0, base_thickness))
    )
    fork_slotted = fork_slotted.cut(slot_cutter)

# 5. Create the cylindrical shaft
# Extrudes downwards from Z=0
shaft = (
    cq.Workplane("XY")
    .circle(shaft_diameter / 2.0)
    .extrude(-shaft_length)
)

# 6. Combine the fork and the shaft
result = fork_slotted.union(shaft)