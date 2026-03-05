import cadquery as cq

# --- Parametric Dimensions ---
total_length = 100.0       # Total length of the assembly (excluding lugs)
cyl_radius = 15.0          # Radius of the main cylinder body
flange_radius = 22.0       # Radius of the end caps/flanges
flange_thickness = 12.0    # Thickness of the end caps
lug_width = 12.0           # Width of the mounting lugs
lug_thickness = 10.0       # Thickness (protrusion) of the lugs
lug_hole_dia = 6.0         # Diameter of the mounting hole
lug_top_height = 8.0       # Height of the lug block above the flange radius
lug_overlap = 10.0         # Length of the lug block resting on the flange

# --- 1. Main Cylinder Body ---
# Centered at origin, aligned with X axis
# extrude(both=True) doubles the length, so we divide by 2
main_body = (
    cq.Workplane("YZ")
    .circle(cyl_radius)
    .extrude(total_length / 2.0, both=True)
)

# --- 2. End Flanges ---
# Left Flange: Positioned at the negative end
flange_left = (
    cq.Workplane("YZ")
    .workplane(offset=-total_length / 2.0)
    .circle(flange_radius)
    .extrude(flange_thickness)
)

# Right Flange: Positioned at the positive end (offset ensures it stays within length)
flange_right = (
    cq.Workplane("YZ")
    .workplane(offset=total_length / 2.0 - flange_thickness)
    .circle(flange_radius)
    .extrude(flange_thickness)
)

# --- 3. Mounting Lugs ---
def create_lug(is_right_side=True):
    """Creates the L-shaped mounting lug for either side."""
    direction = 1 if is_right_side else -1
    
    # The X-coordinate of the outer face of the flange
    face_x = (total_length / 2.0) * direction
    
    # A. Vertical Part (The plate with the hole)
    # Sketch on the end face of the flange
    wp_face = cq.Workplane("YZ").workplane(offset=face_x)
    
    # Calculate top Z height relative to center
    top_z = flange_radius + lug_top_height
    
    # Draw profile: Rectangle from top down to Z=0, then rounded bottom
    lug_profile = (
        wp_face
        .moveTo(-lug_width / 2.0, 0)
        .lineTo(-lug_width / 2.0, top_z)
        .lineTo(lug_width / 2.0, top_z)
        .lineTo(lug_width / 2.0, 0)
        # Create full semicircle at the bottom centered at (0,0)
        .threePointArc((0, -lug_width / 2.0), (-lug_width / 2.0, 0))
        .close()
    )
    
    # Extrude outwards from the cylinder
    lug_solid = lug_profile.extrude(lug_thickness * direction)
    
    # Cut the mounting hole (Transverse axis / Y-axis)
    # We select a side face perpendicular to Y to drill through
    lug_solid = (
        lug_solid
        .faces("<Y")
        .workplane()
        .circle(lug_hole_dia / 2.0)
        .cutThruAll()
    )
    
    # B. Top Block (The connection to the flange)
    # This part sits on the cylindrical surface of the flange
    # We sink it slightly (2mm) into the flange to ensuring a clean solid union
    sink_depth = 2.0
    block_h = lug_top_height + sink_depth
    # Calculate center Z to position the box correctly
    block_z_center = flange_radius - sink_depth + (block_h / 2.0)
    # Calculate center X to position the overlap inwards
    block_x_center = face_x - (lug_overlap / 2.0 * direction)
    
    top_block = (
        cq.Workplane("XY")
        .workplane(offset=block_z_center)
        .center(block_x_center, 0)
        .box(lug_overlap, lug_width, block_h)
    )
    
    return lug_solid.union(top_block)

# Create lugs for both sides
lug_right = create_lug(is_right_side=True)
lug_left = create_lug(is_right_side=False)

# --- 4. Final Assembly ---
result = (
    main_body
    .union(flange_left)
    .union(flange_right)
    .union(lug_right)
    .union(lug_left)
)