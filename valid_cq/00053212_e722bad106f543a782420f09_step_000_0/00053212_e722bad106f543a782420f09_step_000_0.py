import cadquery as cq

# --- Parameters ---
length = 160.0
width = 50.0
base_height = 2.0
rim_height = 4.0
wall_thickness = 3.0
leg_radius = 20.0
leg_thickness = 3.0
divider_ratio = 0.72  # Position of the divider (0-1)
notch_width = 4.0
notch_depth = 2.0
fillet_radius = 1.0

# --- Geometry Construction ---

# 1. Create the Base and Rim Block
# Start with a solid block representing the full outer volume of the tray
tray_base = cq.Workplane("XY").box(length, width, base_height)
tray_rim_block = tray_base.faces(">Z").workplane().box(length, width, rim_height, combine=True)

# 2. Create Compartments (Pockets)
# We create two pockets separated by a wall based on the divider_ratio
split_x = -length/2 + (length * divider_ratio)
pocket_width = width - 2 * wall_thickness

# Large Compartment Dimensions
p1_start = -length/2 + wall_thickness
p1_end = split_x - wall_thickness/2
p1_length = p1_end - p1_start
p1_center = (p1_start + p1_end) / 2

# Small Compartment Dimensions
p2_start = split_x + wall_thickness/2
p2_end = length/2 - wall_thickness
p2_length = p2_end - p2_start
p2_center = (p2_start + p2_end) / 2

# Cut the pockets
tray_hollow = (
    tray_rim_block.faces(">Z").workplane()
    .center(p1_center, 0).rect(p1_length, pocket_width).cutBlind(-rim_height)
    .faces(">Z").workplane()
    .center(p2_center, 0).rect(p2_length, pocket_width).cutBlind(-rim_height)
)

# 3. Create Side Notches
# Small cutouts on the top of the side rails at the divider location
tray_notched = (
    tray_hollow.faces(">Z").workplane()
    # Notch on Top Rail (+Y)
    .center(split_x, width/2).rect(notch_width, wall_thickness * 2).cutBlind(-notch_depth)
    # Notch on Bottom Rail (-Y)
    .faces(">Z").workplane()
    .center(split_x, -width/2).rect(notch_width, wall_thickness * 2).cutBlind(-notch_depth)
)

# 4. Create Legs
# Semi-cylindrical supports at the ends of the tray
z_attach = -base_height / 2

def create_leg(x_center):
    """Creates a semi-cylindrical leg extruded along the Y axis."""
    return (
        cq.Workplane("XZ")
        .workplane(offset=-width/2)  # Start from the back Y-face
        .center(x_center, z_attach)
        .moveTo(leg_radius, 0)
        .threePointArc((0, -leg_radius), (-leg_radius, 0))  # Outer arc (downwards)
        .lineTo(-leg_radius + leg_thickness, 0)             # Connect to inner shell
        .threePointArc((0, -leg_radius + leg_thickness), 
                       (leg_radius - leg_thickness, 0))     # Inner arc (upwards return)
        .close()
        .extrude(width)
    )

# Leg positions align the outer curve tangent to the tray ends
leg_left = create_leg(-length/2 + leg_radius)
leg_right = create_leg(length/2 - leg_radius)

# Union legs with the main body
result = tray_notched.union(leg_left).union(leg_right)

# 5. Finishing Touches
# Apply fillets to vertical edges to smooth the design
try:
    result = result.edges("|Z").fillet(fillet_radius)
except Exception:
    # Fallback if fillet fails due to geometry complexity
    pass