import cadquery as cq

# Parameters
length = 65.0        # Total outer length
width = 25.0         # Total outer width
height = 18.0        # Total height
wall_thickness = 1.5 # Shell thickness
corner_radius = 5.0  # Outer corner radius
leg_relief_height = 7.0 # Height of the cutout on the long sides
hook_depth = 1.0     # How far the snap hook protrudes inward
hook_height = 2.0    # Vertical height of the snap hook feature

# 1. Create the main body block with rounded corners
# Oriented with Top at Z=0, extending down to Z=-height
base = (
    cq.Workplane("XY")
    .rect(length, width)
    .extrude(-height)
    .edges("|Z")
    .fillet(corner_radius)
)

# 2. Shell the body to create the container
# Remove the top face (>Z) to open the container
shelled_body = base.faces(">Z").shell(-wall_thickness)

# 3. Create the relief cut on the long sides
# This creates the "legs" on the short ends by removing material from the bottom-middle
cut_length = length - 2 * corner_radius
cut_width = width + 10.0 # Oversize to cut through
cut_z_center = -height + (leg_relief_height / 2.0)

cut_tool = (
    cq.Workplane("XY")
    .workplane(offset=cut_z_center)
    .box(cut_length, cut_width, leg_relief_height)
)

body_with_legs = shelled_body.cut(cut_tool)

# 4. Create Snap Hooks
# Helper function to create the hook geometry on the short ends
def create_hook(direction):
    """
    Creates a wedge-shaped hook.
    direction: 1 for +X side, -1 for -X side
    """
    # Calculate wall position
    x_wall = (length / 2.0 - wall_thickness) * direction
    x_tip = x_wall - (hook_depth * direction) # Protrudes inward
    
    z_bot = -height
    z_top = -height + hook_height
    
    # Define triangle profile in XZ plane (Ramp on bottom face)
    # P1: Wall Bottom
    # P2: Tip Top (Ledge)
    # P3: Wall Top
    pts = [
        (x_wall, z_bot),
        (x_tip, z_top),
        (x_wall, z_top)
    ]
    
    # Extrude along Y. Length matches the straight section of the short wall.
    extrude_len = width - 2 * corner_radius
    
    hook_geo = (
        cq.Workplane("XZ")
        .polyline(pts)
        .close()
        .extrude(extrude_len / 2.0, both=True)
    )
    return hook_geo

# Generate and union the hooks
hook_pos = create_hook(1)
hook_neg = create_hook(-1)

result = body_with_legs.union(hook_pos).union(hook_neg)