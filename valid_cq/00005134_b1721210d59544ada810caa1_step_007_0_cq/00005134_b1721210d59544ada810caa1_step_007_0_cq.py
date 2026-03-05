import cadquery as cq

# --- Parameters ---
# Main Plate
plate_width = 120.0
plate_depth = 80.0
plate_thickness = 3.0
fillet_radius = 4.0
corner_hole_d = 3.5

# Standouts (Small cylindrical posts)
post_height = 8.0
post_diam_outer = 6.0
post_diam_inner = 3.0
post_base_fillet = 3.0 # The conical widening at the base
post_locations = [
    (-30, -25), (30, -25), 
    (-10, 0), (30, 0)
]

# Square Blocks
block_size = 12.0
block_height = 10.0
block_hole_d = 4.0
block_spacing = 16.0
block_start_x = 20.0
block_y = 15.0

# Rail/Guide Feature (The curved L-shape structures)
rail_length_long = 40.0
rail_length_short = 25.0
rail_width = 10.0
rail_height = 12.0
rail_thickness = 3.0
rail_fillet = 8.0 # Large fillet on the inner curve
rail_y = 20.0 # Y position relative to center
rail_gap = 10.0 # Gap between the two rails

# Small Stopper (next to rails)
stop_width = 5.0
stop_depth = 5.0
stop_height = 6.0

# --- Geometry Construction ---

# 1. Base Plate
plate = (
    cq.Workplane("XY")
    .box(plate_width, plate_depth, plate_thickness)
    .edges("|Z")
    .fillet(fillet_radius)
)

# 2. Corner Mounting Holes
plate = (
    plate.faces(">Z")
    .workplane()
    .rect(plate_width - 2*fillet_radius, plate_depth - 2*fillet_radius, forConstruction=True)
    .vertices()
    .hole(corner_hole_d)
)

# 3. Cylindrical Posts
# Function to create a single post with a tapered base
def create_post(loc):
    # Create the main cylinder
    cyl = (
        cq.Workplane("XY")
        .center(loc[0], loc[1])
        .workplane(offset=plate_thickness/2)
        .circle(post_diam_outer/2)
        .extrude(post_height)
    )
    # Add hole
    cyl = cyl.faces(">Z").hole(post_diam_inner)
    
    # Add fillet at base (using a chamfer/fillet operation on the edge connection)
    # Note: CadQuery fillets can fail on complex joins, so sometimes adding a cone at the base is safer.
    # Here we will try filleting the edge where the post meets the plate.
    return cyl

# Create all posts and unite them with the plate
for loc in post_locations:
    p = create_post(loc)
    # To get the nice tapered base shown in the image, we select the bottom edge of the cylinder
    # However, since it's a separate solid right now, we can fillet it *before* unioning or *after*.
    # Let's try adding a cone base for stability and visual match.
    cone = (
         cq.Workplane("XY")
         .center(loc[0], loc[1])
         .workplane(offset=plate_thickness/2)
         .circle(post_diam_outer/2 + post_base_fillet/2)
         .workplane(offset=post_base_fillet)
         .circle(post_diam_outer/2)
         .loft(combine=True)
    )
    p = p.union(cone)
    plate = plate.union(p)


# 4. Square Blocks
# Generate 3 blocks
for i in range(3):
    x_pos = block_start_x + (i * block_spacing)
    
    blk = (
        cq.Workplane("XY")
        .center(x_pos, block_y)
        .workplane(offset=plate_thickness/2)
        .box(block_size, block_size, block_height, centered=(True, True, False))
    )
    # Add hole
    blk = blk.faces(">Z").hole(block_hole_d)
    plate = plate.union(blk)

# 5. Rails (Curved Extrusions)
# We will draw the profile on YZ plane and extrude in X
def create_rail_profile(length):
    # Determine profile shape: An inverted 'L' or curved bracket
    # We'll sketch on YZ plane
    
    # Profile coordinates relative to a local origin
    # Let's draw a shape that looks like the cross-section
    pts = [
        (0, 0),
        (rail_width, 0),
        (rail_width, rail_thickness),
        (rail_thickness, rail_thickness), # Inner corner point before curve
        (rail_thickness, rail_height),
        (0, rail_height)
    ]
    
    # We will create a block and subtract the inner curve
    base_shape = (
        cq.Workplane("YZ")
        .workplane(offset=-length/2)
        .moveTo(0,0)
        .lineTo(rail_width, 0)
        .lineTo(rail_width, rail_height * 0.4) # Short side up
        .radiusArc((rail_thickness, rail_height), -rail_fillet) # Curve to top
        .lineTo(0, rail_height)
        .close()
        .extrude(length)
    )
    return base_shape

# Create Long Rail (Right side of gap)
rail_long = create_rail_profile(rail_length_long)
# Position it. Note: create_rail_profile extrudes centered on X origin of that plane somewhat? 
# No, offset=-length/2 means it extrudes from there to +length/2.
# We need to rotate and move it to the correct spot on the plate.
# The profile was drawn on YZ, extruded in X. Up is Z.
# We need to align the bottom to plate top (plate_thickness/2) and position in X/Y.
# The profile (0,0) is bottom-left corner.
rail_long = rail_long.translate((0, 0, plate_thickness/2)) 
# Move to specific XY location.
# Let's place the gap slightly left of center to match image.
rail_long_x = 5.0 + rail_length_long/2
rail_z_rotation_adj = 180 # Rotate so the curve faces "in" (towards -Y)
rail_long = rail_long.rotate((0,0,0), (0,0,1), 180) # Flip it
rail_long = rail_long.translate((10, rail_y + rail_width, 0)) # Approximate manual placement logic

# Create Short Rail (Left side of gap)
rail_short = create_rail_profile(rail_length_short)
rail_short = rail_short.rotate((0,0,0), (0,0,1), 180) # Flip it
rail_short = rail_short.translate((-35, rail_y + rail_width, plate_thickness/2))

plate = plate.union(rail_long).union(rail_short)

# 6. Small Stoppers
# One at the far left end of the short rail
stop1 = (
    cq.Workplane("XY")
    .center(-35 - rail_length_short/2 - stop_width, rail_y + rail_width/2)
    .workplane(offset=plate_thickness/2)
    .box(stop_width, stop_depth, stop_height, centered=(True, True, False))
)

# One at the right end of the long rail
stop2 = (
    cq.Workplane("XY")
    .center(10 + rail_length_long/2 + stop_width, rail_y + rail_width/2)
    .workplane(offset=plate_thickness/2)
    .box(stop_width, stop_depth, stop_height, centered=(True, True, False))
)

plate = plate.union(stop1).union(stop2)

result = plate