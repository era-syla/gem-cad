import cadquery as cq

# --- Parametric Dimensions ---
# Overall dimensions
overall_width = 40.0
overall_length = 40.0
total_height = 35.0

# Top cap dimensions
cap_thickness = 5.0
cap_overhang = 2.0  # How much the cap extends past the main body

# Main body dimensions
body_width = overall_width - (2 * cap_overhang)
body_length = overall_length - (2 * cap_overhang)
body_height = total_height - cap_thickness

# Arch/Cutout dimensions
arch_width = body_width * 0.7
arch_height = body_height * 0.7  # Height of the arch from the bottom

# Snap/Hook detail at the bottom
hook_depth = 3.0  # How far the hook sticks out
hook_height = 5.0  # Vertical size of the hook
hook_taper_height = 5.0

# --- Modeling Strategy ---
# 1. Create the top cap (a simple box).
# 2. Create the main body block underneath it.
# 3. Create the arched cutout through the body.
# 4. Add the wedge/hook features at the bottom of the legs.

# 1. Top Cap
# Centered on XY plane, extruded upwards
cap = cq.Workplane("XY").box(overall_width, overall_length, cap_thickness)

# 2. Main Body
# Create a block attached to the bottom of the cap
# We move down by cap_thickness/2 + body_height/2 to position it correctly relative to the cap center
body = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, -cap_thickness/2 - body_height/2))
    .box(body_width, body_length, body_height)
)

# 3. Arch Cutout
# We'll cut a shape from the front face (XZ plane relative to the body)
# Or easier: Create a profile on the side and extrude-cut.
# Let's use a cylinder cut for a perfect circular arch, or a custom sketch for a specific arch.
# Looking at the image, it seems like a circular arc top with straight sides, or a full semi-circle.
# Let's assume a "tunnel" cut along the Y-axis.

# Create the profile for the cut on the XZ plane
# Positioned at the bottom of the body
cut_profile = (
    cq.Workplane("XZ")
    .transformed(offset=(0, -total_height/2 + cap_thickness/2, 0)) # roughly centering on Z
)

# Actually, let's just make the cut relative to the global origin.
# The bottom of the assembly is at Z = -cap_thickness/2 - body_height = -total_height + cap_thickness/2 roughly.
# Let's rethink the Z-positioning to make it easier. Let Z=0 be the bottom of the legs.

# --- Revised Modeling Strategy (Z=0 at bottom) ---

# 1. Top Cap
top_cap = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, total_height - cap_thickness/2))
    .box(overall_width, overall_length, cap_thickness)
)

# 2. Main Body (before cut)
main_block = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, (total_height - cap_thickness)/2))
    .box(body_width, body_length, total_height - cap_thickness)
)

# 3. Arch Cutout (Tunnel)
# Cylindrical cut along Y axis. Center of cylinder is at Z = some height.
# Looking at the image, the arch goes all the way through.
# It looks like a simple semi-circle or an arc. Let's try a cylinder centered slightly below the arch apex.
radius = arch_width / 2.0
# Center the cylinder on the bottom face so the top of the cylinder forms the arch
cutout = (
    cq.Workplane("XZ")
    .transformed(offset=(0, radius, 0)) # Move center up by radius to create semi-circle at bottom
    .circle(radius)
    .extrude(overall_length * 2) # Cut through everything
)

# Refined cutout: The image shows straight vertical walls for the tunnel before the curve starts.
# So we need a U-shape sketch.
cutout_shape = (
    cq.Workplane("YZ") # Drawing on the side plane
    .transformed(offset=(0, 0, 0))
    .moveTo(-body_length, 0) # Start outside
    .lineTo(body_length, 0)
    .lineTo(body_length, arch_height - radius)
    .threePointArc((0, arch_height), (-body_length, arch_height - radius))
    .close()
    .extrude(overall_width) # This creates a solid to intersect or we rotate coordinates.
)
# Actually, the simplest way for a tunnel along Y axis:
tunnel_cut = (
    cq.Workplane("XZ")
    .moveTo(-arch_width/2, 0)
    .lineTo(-arch_width/2, arch_height - arch_width/2)
    .threePointArc((0, arch_height), (arch_width/2, arch_height - arch_width/2))
    .lineTo(arch_width/2, 0)
    .close()
    .extrude(overall_length + 10, both=True) # Cut through Y
)

# 4. Snap Hooks
# These are triangular prisms on the outside bottom edges of the 'legs' (along Y).
# We can sketch them on the XZ plane and extrude.
hook_sketch = (
    cq.Workplane("XZ")
    .moveTo(body_width/2, 0)
    .lineTo(body_width/2 + hook_depth, hook_height)
    .lineTo(body_width/2, hook_height + hook_taper_height)
    .close()
    # Mirror for the other side
    .moveTo(-body_width/2, 0)
    .lineTo(-(body_width/2 + hook_depth), hook_height)
    .lineTo(-body_width/2, hook_height + hook_taper_height)
    .close()
    .extrude(body_length / 2, both=True)
)

# Combine parts
result = (
    top_cap
    .union(main_block)
    .cut(tunnel_cut)
    .union(hook_sketch)
)

# Optional: Add fillets to the hook edge to match image "softness" slightly if needed, 
# but sharp corners appear in the diagram for the main geometry. 
# The top cap overhang looks sharp.