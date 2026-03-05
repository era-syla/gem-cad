import cadquery as cq

# --- Parametric Dimensions ---

# Main Body (Box) Dimensions
box_length = 260.0
box_width = 40.0
box_height = 45.0

# Base Dimensions
base_thick = 3.0
flange_width = 3.0  # Width of the rim around the box
base_l = box_length + 2 * flange_width
base_w = box_width + 2 * flange_width

# Side Platform Dimensions
plat_length = 90.0
plat_width = 60.0   # Total width of the side plate
plat_thick = base_thick

# Handle Dimensions
handle_spacing = 110.0  # Distance between the two handles
h_width = 16.0
h_height = 14.0
h_thick = 1.2
h_pad_size = 5.0
h_pad_thick = 1.0

# --- Geometry Construction ---

# 1. Create the Base Assembly
# Main rectangular base footprint
base_main = (
    cq.Workplane("XY")
    .box(base_l, base_w, base_thick, centered=(True, True, False))
)

# Side extension plate
# Calculate Y-offset to attach to the side of the main base
# Attaching to the -Y side
overlap = 2.0  # Ensure solid intersection for union
plat_center_y = -(base_w / 2) - (plat_width / 2) + overlap

side_plate = (
    cq.Workplane("XY")
    .center(0, plat_center_y)
    .box(plat_length, plat_width, plat_thick, centered=(True, True, False))
)

base_assembly = base_main.union(side_plate)

# 2. Create the Main Enclosure Box
# Extruded up from the top of the base
main_box = (
    cq.Workplane("XY")
    .workplane(offset=base_thick)
    .box(box_length, box_width, box_height, centered=(True, True, False))
)

# 3. Create Handles
def create_handle():
    """Generates a U-shaped handle with mounting pads."""
    
    # Create mounting pads
    pad = cq.Workplane("XY").box(h_pad_size, h_pad_size, h_pad_thick, centered=(True, True, False))
    pads = (
        pad.translate((-h_width/2, 0, 0))
        .union(pad.translate((h_width/2, 0, 0)))
    )
    
    # Create the wire path
    # Using a polyline with arc fillets for the U-shape in the XZ plane
    fillet_r = 3.0
    
    # Path coordinates (local to handle center)
    # Start at top of left pad, go up, arc right, go down to right pad
    p_start = (-h_width/2, h_pad_thick)
    p_end = (h_width/2, h_pad_thick)
    
    path = (
        cq.Workplane("XZ")
        .moveTo(p_start[0], p_start[1])
        .lineTo(-h_width/2, h_height - fillet_r)
        .radiusArc((-h_width/2 + fillet_r, h_height), fillet_r)
        .lineTo(h_width/2 - fillet_r, h_height)
        .radiusArc((h_width/2, h_height - fillet_r), fillet_r)
        .lineTo(p_end[0], p_end[1])
    )
    
    # Create profile for sweep (Circle on XY plane, centered at start of path)
    profile = (
        cq.Workplane("XY")
        .workplane(offset=h_pad_thick)
        .center(-h_width/2, 0)
        .circle(h_thick/2)
    )
    
    wire = profile.sweep(path)
    
    return pads.union(wire)

# Generate a single handle geometry
handle_geo = create_handle()

# Position handles on top of the main box
z_top = base_thick + box_height
h1 = handle_geo.translate((-handle_spacing/2, 0, z_top))
h2 = handle_geo.translate((handle_spacing/2, 0, z_top))

# --- Final Boolean Union ---
result = base_assembly.union(main_box).union(h1).union(h2)