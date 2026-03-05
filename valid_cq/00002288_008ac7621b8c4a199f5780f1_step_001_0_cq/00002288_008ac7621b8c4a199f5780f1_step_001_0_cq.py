import cadquery as cq

# --- Parametric Dimensions ---
# Overall Plate Dimensions
plate_length = 80.0
plate_width = 40.0
plate_thickness = 2.0

# Leg/Hook Dimensions
leg_width = 5.0
leg_height = 8.0  # Height from plate bottom
leg_hook_length = 3.0  # Length of the hook overhang
leg_thickness = 2.0
leg_chamfer = 2.0 # Chamfer on the hook corners

# Hexagonal Grid Pattern
hex_radius = 2.0  # Outer radius of the hexagon
hex_spacing_x = 6.0  # Distance between centers in X
hex_spacing_y = 5.0 # Distance between centers in Y (rows)
hex_rotation = 30 # Rotate hexagons so point is up/down

# --- Geometry Construction ---

# 1. Create the Main Plate
plate = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# 2. Create the Legs/Hooks
# We will define a profile for one leg and sweep or extrude it, then mirror/place them.
# Let's create a single leg profile on the side face.

def create_hook(loc_x, loc_y):
    # Determine direction based on location
    direction_x = 1 if loc_x > 0 else -1
    direction_y = 1 if loc_y > 0 else -1
    
    # We will build the hook by drawing a 2D profile on the XZ plane (side view)
    # and extruding it along Y.
    
    # Profile points relative to the corner of the plate
    # Starting at the bottom corner of the plate
    pts = [
        (0, 0),
        (0, -leg_height),
        (leg_thickness + leg_hook_length, -leg_height),
        (leg_thickness + leg_hook_length, -leg_height + leg_thickness),
        (leg_thickness, -leg_height + leg_thickness),
        (leg_thickness, 0)
    ]
    
    # Create the profile
    # Position the workplane on the appropriate face
    wp = (
        cq.Workplane("XZ")
        .center(loc_x * (plate_length/2), -plate_thickness/2) # Start at corner
    )
    
    # Adjust orientation if on the negative X side
    if direction_x < 0:
        wp = wp.mirror("YZ")
        
    hook = (
        wp
        .polyline(pts)
        .close()
        .extrude(leg_width * -direction_y) # Extrude inward towards plate center or outward depending on logic
    )
    
    # Reposition extrusion if needed to align with corner exactly
    # The extrusion starts at Y=0 (center), we need it at the edge Y (+/- width/2)
    
    offset_y = (plate_width/2 - leg_width) if direction_y > 0 else -(plate_width/2 - leg_width)
    # Actually simpler: The Workplane is at Y=0. Let's move it.
    
    return hook

# Alternative Leg Strategy: Construct one, mirror it around.
# Profile on XZ plane.
leg_profile = (
    cq.Workplane("XZ")
    .polyline([
        (0, 0),
        (0, -leg_height),
        (leg_thickness + leg_hook_length, -leg_height),
        (leg_thickness + leg_hook_length, -leg_height + leg_thickness),
        (leg_thickness, -leg_height + leg_thickness),
        (leg_thickness, 0),
        (0,0)
    ])
    .close()
)

# Extrude the leg profile. 
# We position it at the corner: x = length/2, y = width/2
leg_solid = (
    leg_profile
    .extrude(leg_width) # Extrudes along positive Y
)

# Now we need to orient and place 4 copies.
# The initial leg is built at Origin, extending +X and -Z, extruded +Y.
# We move it to the correct corner relative to the plate.
# Plate center is (0,0,0). Plate top is Z=plate_thickness/2, Bottom Z=-plate_thickness/2.
# Leg starts at bottom edge.

# Leg 1: Top Right (+X, +Y)
# Rotate so it points outwards? The image shows hooks pointing INWARD relative to the long axis?
# Looking at the image: 
# The legs are on the short edges (width).
# The "hook" part points OUTWARDS from the main body length-wise.
# The leg extends DOWN from the plate.

# Let's redefine the profile to match the image better.
# Profile on XZ plane, drawn on the right face (+X).
hook_profile = (
    cq.Workplane("XZ")
    .workplane(offset=plate_width/2 - leg_width) # Move to near the edge
    .moveTo(plate_length/2, -plate_thickness/2)
    .lineTo(plate_length/2, -plate_thickness/2 - leg_height)
    .lineTo(plate_length/2 - leg_hook_length, -plate_thickness/2 - leg_height)
    .lineTo(plate_length/2 - leg_hook_length, -plate_thickness/2 - leg_height + leg_thickness)
    .lineTo(plate_length/2 - leg_thickness, -plate_thickness/2 - leg_height + leg_thickness)
    .lineTo(plate_length/2 - leg_thickness, -plate_thickness/2)
    .close()
)

leg1 = hook_profile.extrude(leg_width)

# Add Chamfer to the hook tip (bottom outer corner)
# We need to select the edge.
# The leg is at X positive. The hook points -X (inward under plate).
# Wait, looking at image again.
# The hooks stick OUT along the Y axis? Or X axis?
# It looks like the hooks are on the corners.
# Let's assume the long dimension is X.
# The hooks are on the ends of the long dimension.
# They point INWARDS towards the center of the plate (underneath).
# The profile I just drew does exactly that.
# Let's chamfer the outer bottom corner of the leg.
# This corresponds to the point (plate_length/2, -plate_thickness/2 - leg_height).
leg1 = leg1.edges(cq.selectors.BoxSelector(
    (plate_length/2 - 0.1, -plate_width, -plate_thickness/2 - leg_height - 0.1),
    (plate_length/2 + 0.1, plate_width, -plate_thickness/2 - leg_height + leg_thickness + 0.1)
)).chamfer(leg_chamfer)


# Create the 4 legs by mirroring
leg2 = leg1.mirror("XZ") # Mirror to other side of Y
leg3 = leg1.mirror("YZ") # Mirror to other side of X
leg4 = leg3.mirror("XZ") # Mirror that one to other side of Y

legs = leg1.union(leg2).union(leg3).union(leg4)

# Combine Plate and Legs
result_solid = plate.union(legs)

# 3. Create Hexagonal Perforations
# We need a grid of points.
# Staggered grid logic.

pts = []
# Calculate number of columns and rows based on plate size and margins
margin_x = 10.0
margin_y = 8.0

x_start = -plate_length/2 + margin_x
x_end = plate_length/2 - margin_x
y_start = -plate_width/2 + margin_y
y_end = plate_width/2 - margin_y

# Generate points
current_y = y_start
row_index = 0

while current_y <= y_end:
    current_x = x_start
    
    # Shift every other row
    if row_index % 2 == 1:
        current_x += hex_spacing_x / 2
        
    while current_x <= x_end:
        # Check bounds again for staggered rows to ensure we don't bleed out
        if current_x <= x_end:
            pts.append((current_x, current_y))
        current_x += hex_spacing_x
        
    current_y += hex_spacing_y
    row_index += 1

# Cut the hexagons
result = (
    result_solid
    .faces(">Z")
    .workplane()
    .pushPoints(pts)
    .polygon(6, hex_radius * 2, circumscribed=True) # CadQuery polygon takes diameter
    .cutBlind(-plate_thickness)
)

# Export or Render
if 'show_object' in globals():
    show_object(result)