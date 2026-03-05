import cadquery as cq

# --- Parameters ---
length = 140.0       # Total length of the top edge
height = 35.0        # Max vertical depth
thickness = 3.0      # Material thickness
fillet_outer = 5.0   # Radius for outer contour fillets
fillet_inner = 3.0   # Radius for internal cutout fillets
nut_dia = 6.4        # Circumscribed diameter for M3 nut pocket
nut_depth = 1.8      # Depth of the nut recess
hole_dia = 3.2       # Diameter for M3 screw holes

# --- 1. Base Geometry ---
# Define points for the outer contour (clockwise starting top-left)
# Coordinates centered horizontally on the top edge
pts_outer = [
    (-length/2, 0),                 # Top Left
    (length/2, 0),                  # Top Right
    (length/2, -8),                 # Right vertical drop
    (length/2 - 25, -height),       # Right Lobe Tip
    (0, -16),                       # Center Bridge (Valley)
    (-(length/2 - 25), -height),    # Left Lobe Tip
    (-length/2, -8)                 # Left vertical drop
]

# Create the main solid plate
base = (
    cq.Workplane("XY")
    .polyline(pts_outer)
    .close()
    .extrude(thickness)
    .edges("|Z")            # Select all vertical edges
    .fillet(fillet_outer)   # Apply rounded corners
)

# --- 2. Internal Cutouts ---
# Define points for the weight-reduction cutouts
# Right Cutout (Trapezoidal shape)
pts_cut_r = [
    (15, -10),
    (length/2 - 15, -10),
    (length/2 - 32, -height + 8),
    (25, -24)
]

# Left Cutout (Mirrored X coordinates)
pts_cut_l = [
    (-15, -10),
    (-(length/2 - 15), -10),
    (-(length/2 - 32), -height + 8),
    (-25, -24)
]

# Generate cutout solids
cutters = (
    cq.Workplane("XY")
    .polyline(pts_cut_r).close()
    .polyline(pts_cut_l).close()
    .extrude(thickness)
    .edges("|Z")
    .fillet(fillet_inner)   # Round the corners of the cutouts
)

# Subtract cutouts from the base
result = base.cut(cutters)

# --- 3. Mounting Features ---
# Coordinates for mounting points estimated from image
# Right Lobe
r_top_pos = (42, -13)
r_bot_pos = (52, -28)
# Left Lobe
l_top_pos = (-42, -13)
l_bot_pos = (-52, -28)

def add_mount_point(part, x, y, has_hex_recess=False):
    """Adds a screw hole, optionally with a hexagonal nut recess."""
    wp = part.faces(">Z").workplane().center(x, y)
    
    if has_hex_recess:
        # Cut hex pocket
        wp = wp.polygon(6, nut_dia).cutBlind(-nut_depth)
        # Re-center for the through hole (workplane context shifts after cut)
        wp = part.faces(">Z").workplane().center(x, y)
        
    # Cut through hole
    return wp.hole(hole_dia)

# Apply features
result = add_mount_point(result, *r_top_pos, has_hex_recess=True)
result = add_mount_point(result, *r_bot_pos, has_hex_recess=False)
result = add_mount_point(result, *l_top_pos, has_hex_recess=True)
# The bottom-left feature looks like a recess/slot in the image
result = add_mount_point(result, *l_bot_pos, has_hex_recess=True)

# --- 4. Final Polish ---
# Add a small chamfer to the top face edges for a finished look
result = result.edges(">Z").chamfer(0.2)