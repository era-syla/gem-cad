import cadquery as cq

# --- Parametric Dimensions ---
length = 90.0        # Total length of the part
width = 34.0         # Total width of the part
height = 18.0        # Total height of the part
thickness = 2.0      # Wall thickness
fillet_rad = 6.0     # Radius of vertical corners
hook_depth = 2.5     # How far the clips protrude inwards
hook_height = 4.0    # Vertical size of the hook lip
arch_rise = 3.0      # Height of the arch cut at the bottom center

# --- 1. Create Base Solid ---
# Create a rectangular block and fillet the vertical edges
base = (
    cq.Workplane("XY")
    .box(length, width, height)
    .edges("|Z")
    .fillet(fillet_rad)
)

# --- 2. Create Bottom Arch Cut ---
# Calculate the radius of a circle that corresponds to the desired arch rise
# for the given width. Alternatively, use a fixed large radius.
# Here we define a large cylinder to cut the bottom face, creating the arch.
# The cylinder is oriented along the X-axis (Length).
cylinder_radius = (width**2 / (8 * arch_rise)) + (arch_rise / 2)
cylinder_center_z = -height/2.0 - cylinder_radius + arch_rise

cutter = (
    cq.Workplane("YZ")
    .workplane(offset=-length)  # Position start of cut
    .center(0, cylinder_center_z)
    .circle(cylinder_radius)
    .extrude(length * 2)        # Cut through the entire length
)

base_arched = base.cut(cutter)

# --- 3. Shell the Solid ---
# Remove the top face to create the container walls
# A negative thickness offsets inwards
shell = base_arched.faces("+Z").shell(-thickness)

# --- 4. Create Retention Hooks ---
# We define the hook profile (a wedge shape) on the XZ plane and extrude it.
# Then we intersect it with the base shape to trim it to the rounded corners.

# Right Hook Points (+X end)
p_x_out = length / 2.0
p_x_in = p_x_out - thickness - hook_depth
p_z_top = height / 2.0
p_z_bot = p_z_top - hook_height

right_hook_pts = [
    (p_x_out, p_z_top),
    (p_x_out, p_z_bot),
    (p_x_in, p_z_top)
]

# Left Hook Points (-X end)
p_x_out_L = -length / 2.0
p_x_in_L = p_x_out_L + thickness + hook_depth

left_hook_pts = [
    (p_x_out_L, p_z_top),
    (p_x_out_L, p_z_bot),
    (p_x_in_L, p_z_top)
]

# Extrude the hook profiles
# We extrude wider than the part width to ensure full coverage
raw_hooks = (
    cq.Workplane("XZ")
    .polyline(right_hook_pts).close()
    .polyline(left_hook_pts).close()
    .extrude(width * 1.5, both=True)
)

# Trim the hooks to fit strictly within the outer boundary of the base shape
# This ensures the hooks follow the corner fillets perfectly
fitted_hooks = raw_hooks.intersect(base_arched)

# --- 5. Combine to Final Result ---
result = shell.union(fitted_hooks)

# Export or visualization would happen here in a typical workflow
# show_object(result)