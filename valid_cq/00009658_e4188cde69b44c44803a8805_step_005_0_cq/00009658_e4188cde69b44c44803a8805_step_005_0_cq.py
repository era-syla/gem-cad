import cadquery as cq

# Parameters
# Top rail dimensions
rail_length = 100.0
rail_width = 20.0
rail_height = 5.0
channel_depth = 3.0
channel_width = 14.0
lip_width = 2.0  # Width of the top edges

# Support block dimensions
block_length = 20.0
block_width = 20.0
block_height = 15.0  # Height below the rail
arch_radius = 6.0    # Radius of the cutout at the bottom
block_spacing = 30.0 # Distance between the two blocks

# --- Construction ---

# 1. Create the Profile for the Top Rail
# We draw the cross-section on the YZ plane (or XZ) and extrude along X (or Y).
# Let's align length along X.
# (0,0) will be the center bottom of the rail.

# Calculate points for the rail profile
r_half_w = rail_width / 2.0
c_half_w = channel_width / 2.0
floor_thickness = rail_height - channel_depth

def create_rail_profile():
    p = (
        cq.Workplane("YZ")
        .moveTo(-r_half_w, 0)
        .lineTo(r_half_w, 0)                # Bottom flat
        .lineTo(r_half_w, rail_height)      # Right outer wall up
        .lineTo(c_half_w, rail_height)      # Right top lip in
        .lineTo(c_half_w, floor_thickness)  # Right inner wall down
        .lineTo(-c_half_w, floor_thickness) # Channel floor
        .lineTo(-c_half_w, rail_height)     # Left inner wall up
        .lineTo(-r_half_w, rail_height)     # Left top lip out
        .close()
    )
    return p

rail_profile = create_rail_profile()
rail = rail_profile.extrude(rail_length)

# Center the rail along X
rail = rail.translate((-rail_length / 2.0, 0, 0))


# 2. Create a Single Support Block
# This block sits underneath the rail.
# We'll make a rectangle and cut an arch out of it.

def create_block():
    # Base block
    b = (
        cq.Workplane("XY")
        .rect(block_length, block_width)
        .extrude(-block_height) # Extrude downwards
    )
    
    # Create the arch cut
    # We'll draw a circle on the face and cut it
    cut_solid = (
        cq.Workplane("YZ")
        .circle(arch_radius)
        .extrude(block_length * 2) # Make it long enough to cut through
    )
    
    # Move the cylinder to the bottom center of the block
    # Since the block was extruded -block_height from Z=0, the bottom is at Z=-block_height
    cut_solid = cut_solid.translate((0, 0, -block_height))
    
    # Perform the cut
    b = b.cut(cut_solid)
    return b

base_block = create_block()

# 3. Position and Combine
# The rail is centered at X=0.
# We need two blocks. Let's assume the gap in the image implies a specific spacing.
# Looking at the image, there is a distinct gap between the blocks, and the rail continues over them.
# There is also a detached piece on the right in the image, but the prompt asks for "this 3D CAD model".
# The detached piece looks identical to one of the support blocks + a segment of rail.
# However, standard interpretation of such an image is usually a single assembly or a "broken view".
# Let's interpret the image as a single rail with two support blocks, and a separate loose piece to show the profile.
# BUT, looking closer, the gap is a physical break in the rail. It looks like two separate components aligned.
# Component A: Long rail with one block in the middle/left.
# Component B: Short rail segment with one block.
# Or, it's an assembly of a long rail on two blocks, and the image is "exploded" or just shows two separate instances.
# Given the "result" requirement, let's model the main assembly (Long Rail + Left Block) and the secondary piece (Short Rail + Right Block) as seen in the image, keeping their relative positions.

# Let's approximate the positions based on the visual.
# Left assembly: Long rail, one block.
# Right assembly: Short rail, one block.

# Left Assembly (Longer Rail)
left_rail_len = 60.0
left_rail = create_rail_profile().extrude(left_rail_len).translate((-left_rail_len/2, 0, 0))

# Left Block (Centered under left rail for simplicity, or slightly offset)
left_block = base_block.translate((0, 0, 0)) # Already centered at X=0, Y=0

# Move left assembly slightly to the left to match image composition
left_assembly = left_rail.union(left_block).translate((-15, 0, 0))


# Right Assembly (Short piece)
right_rail_len = block_length # Same length as the block
right_rail = create_rail_profile().extrude(right_rail_len).translate((-right_rail_len/2, 0, 0))
right_block = base_block # Centered at 0,0
right_assembly = right_rail.union(right_block)

# Move right assembly to the right to create the gap
gap_size = 10.0
# Calculate position: Left assembly ends at (roughly) -15 + 30 = 15.
# Let's just spacing them visually.
right_assembly = right_assembly.translate((35, 0, 0))

# Combine everything into one object
result = left_assembly.union(right_assembly)