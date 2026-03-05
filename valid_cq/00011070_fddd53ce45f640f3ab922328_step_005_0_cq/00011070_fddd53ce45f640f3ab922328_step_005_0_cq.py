import cadquery as cq

# --- Parametric Variables ---
# Rail dimensions
rail_length = 300.0
rail_width = 15.0
rail_height = 12.0
groove_depth = 4.0
groove_width = 4.0
hole_pitch = 60.0  # Distance between mounting holes
hole_diameter = 3.5
cbr_diameter = 6.0
cbr_depth = 3.5
end_margin = 15.0  # Distance from end to first hole

# Carriage (Block) dimensions
block_length = 45.0
block_width = 34.0
block_height = 24.0  # Total height from bottom of rail
block_body_height = block_height - rail_height + 4.0 # Estimate block body itself
mounting_hole_spacing_x = 26.0
mounting_hole_spacing_y = 26.0
block_hole_dia = 3.2 # M3 tapping size approx

# --- Rail Construction ---

# 1. Create the profile of the rail
# The profile looks roughly like a rectangle with side grooves for balls
def create_rail_profile():
    base_w = rail_width
    base_h = rail_height
    
    # Coordinates for a generic linear rail cross-section
    # (Simplified representation of an MGN-style rail)
    pts = [
        (-base_w/2, 0),
        (base_w/2, 0),
        (base_w/2, base_h * 0.4), # Bottom flange
        (base_w/2 * 0.6, base_h * 0.5), # Indent
        (base_w/2, base_h * 0.6), # Top flange start
        (base_w/2, base_h),
        (-base_w/2, base_h),
        (-base_w/2, base_h * 0.6),
        (-base_w/2 * 0.6, base_h * 0.5), # Indent
        (-base_w/2, base_h * 0.4),
        (-base_w/2, 0)
    ]
    return cq.Workplane("XY").polyline(pts).close()

rail_profile = create_rail_profile()
rail = rail_profile.extrude(rail_length)

# 2. Add mounting holes to the rail
# Calculate hole positions
num_holes = int((rail_length - 2 * end_margin) / hole_pitch) + 1
hole_positions = []
for i in range(num_holes):
    # Centered along Y (length), so offset from center
    # Z-axis is the length in default extrude, but let's reorient mentally.
    # The extrusion happened along Z.
    pos_z = end_margin + i * hole_pitch
    hole_positions.append((0, pos_z))

# We need to orient the workplane to drill into the top of the rail
# The rail was extruded along Z, so the top face is likely parallel to XY but "up" isn't strictly defined yet.
# Let's rotate the rail so it lies along X for easier reasoning, matching the image.
rail = rail.rotate((0,0,0), (1,0,0), 90).rotate((0,0,0), (0,0,1), -90)

# Now Rail: Length along X, Width along Y, Height along Z.
# Re-calculate hole positions for X-axis alignment
hole_positions_x = []
start_x = -rail_length / 2 + end_margin
for i in range(num_holes):
    hole_positions_x.append((start_x + i * hole_pitch, 0))

rail = (rail
        .faces(">Z")
        .workplane()
        .pushPoints(hole_positions_x)
        .cboreHole(hole_diameter, cbr_diameter, cbr_depth)
       )

# --- Carriage (Block) Construction ---

# 1. Main Block Body
block = cq.Workplane("XY").box(block_length, block_width, block_body_height)

# 2. Cut out the slot for the rail to pass through
# The slot needs to match the rail profile roughly
slot_width = rail_width + 0.5 # Clearance
slot_height = rail_height 
block = (block
         .faces("-Z")
         .workplane()
         .rect(block_length + 2, slot_width) # Cut through entire length
         .cutBlind(-slot_height + 2) # Cut up into the block, leaving top material
        )

# 3. Add mounting holes to the block
# Standard 4-hole pattern
block_holes = [
    (mounting_hole_spacing_x/2, mounting_hole_spacing_y/2),
    (mounting_hole_spacing_x/2, -mounting_hole_spacing_y/2),
    (-mounting_hole_spacing_x/2, mounting_hole_spacing_y/2),
    (-mounting_hole_spacing_x/2, -mounting_hole_spacing_y/2),
]

block = (block
         .faces(">Z")
         .workplane()
         .pushPoints(block_holes)
         .hole(block_hole_dia, depth=10) # Blind holes
        )

# --- Assembly ---

# Position the block on the rail
# Rail top surface is at Z = rail_height (if base is at 0)
# Let's align them.
# Currently Rail center is at Z = rail_height/2 (roughly) based on rotation
# Let's move rail so bottom is at Z=0
rail = rail.translate((0, 0, rail_height/2))

# Block center is at Z=0. We need to move it up.
# Block sits on the rail. The rail height is `rail_height`.
# The block internal cut allows it to sit around the rail.
# We'll position the block near one end, similar to the image.
block_x_pos = -rail_length/2 + 60 
block_z_pos = rail_height - (rail_height - block_body_height)/2 + (block_body_height/2) # Approximation for visual stack
# Actually, simpler: The top of the rail is at Z=rail_height. 
# The block usually rides so its top surface is at specific height.
# Let's place the block such that it visually encompasses the rail.
block = block.translate((block_x_pos, 0, rail_height/2 + block_body_height/2))

# Combine for final result
result = rail.union(block)