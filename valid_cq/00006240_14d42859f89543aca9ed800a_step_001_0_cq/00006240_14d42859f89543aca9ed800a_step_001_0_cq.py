import cadquery as cq
import math

# --- Parametric Dimensions ---
total_height = 80.0       # Overall length of the part
outer_radius = 50.0       # Radius of the main cylinder body
wall_thickness = 4.0      # Thickness of the cylinder wall
flange_width = 5.0        # How much wider the flange is than the body
flange_height = 6.0       # Thickness/height of the flange at the base

# Window (cutout) parameters
num_windows = 8           # Number of windows around the circumference
window_width = 15.0       # Arc length or width of the window
window_height = 12.0      # Height of the window along the cylinder axis
window_row_spacing = 30.0 # Distance between the centers of the two rows
row1_z_offset = 30.0      # Distance from base to center of first row

# --- Derived Dimensions ---
inner_radius = outer_radius - wall_thickness
flange_outer_radius = outer_radius + flange_width

# --- Construction ---

# 1. Create the main hollow cylinder body
# We create a solid cylinder and then hollow it out
main_body = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(total_height)
)

# 2. Create the flange at the base
# We add a larger disk at the bottom
flange = (
    cq.Workplane("XY")
    .circle(flange_outer_radius)
    .extrude(flange_height)
)

# Combine body and flange
part = main_body.union(flange)

# 3. Hollow out the cylinder (create the bore)
part = (
    part.faces(">Z")
    .workplane()
    .hole(inner_radius * 2)
)

# 4. Create the Cutouts
# We need to cut rectangular slots through the wall.
# Since the slots are radial, it's easier to create a shape to subtract
# and rotate it around the center axis.

def create_window_cutter(z_pos, angle_offset=0):
    """
    Creates a cutting tool for a single window.
    z_pos: Height along the cylinder.
    angle_offset: Rotation around Z axis.
    """
    # Create a box located at the wall perimeter
    # We position it slightly further out to ensure a clean cut through the wall
    cutter = (
        cq.Workplane("XZ")
        .workplane(offset=outer_radius) # Move plane to the surface
        .center(0, z_pos)               # Position vertically
        .rect(window_width, window_height)
        .extrude(-wall_thickness * 3)   # Cut inwards (negative extrusion)
    )
    
    # Rotate the cutter to the correct angle around Z
    cutter = cutter.rotate((0,0,0), (0,0,1), angle_offset)
    return cutter

# Generate cutouts for the first row
for i in range(num_windows):
    angle = i * (360.0 / num_windows)
    cutter = create_window_cutter(row1_z_offset, angle)
    part = part.cut(cutter)

# Generate cutouts for the second row
# Based on the image, the second row seems aligned with the first row (not staggered)
row2_z_offset = row1_z_offset + window_row_spacing

for i in range(num_windows):
    angle = i * (360.0 / num_windows)
    cutter = create_window_cutter(row2_z_offset, angle)
    part = part.cut(cutter)

# 5. Add a small fillet to the transition between flange and body (optional but good for realism)
# Selecting the edge where the flange meets the body
try:
    part = part.edges(cq.selectors.RadiusNthSelector(1)).fillet(2.0)
except:
    # Fallback if specific edge selection is tricky, usually the edge at z=flange_height
    # Select edges at the specific Z height corresponding to the flange top
    part = part.edges(f"Z almost {flange_height}").fillet(1.0)


result = part