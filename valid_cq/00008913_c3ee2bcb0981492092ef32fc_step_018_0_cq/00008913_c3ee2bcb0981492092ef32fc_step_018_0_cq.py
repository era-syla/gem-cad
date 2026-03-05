import cadquery as cq

# Parametric dimensions
block_length = 40.0
block_width = 20.0
block_height = 25.0

hole_diameter = 10.0
hole_spacing = 20.0  # Center-to-center distance between holes

# Foot/Leg dimensions
foot_width = 3.0
foot_depth = 2.0
foot_height = 5.0
foot_hook_size = 2.0  # Length of the horizontal part of the hook
foot_hook_height = 2.0 # Height of the angled part of the hook

# Calculations for positioning
hole_y_offset = 0  # Centered on width
hole_x_offset = hole_spacing / 2.0

# Create the main block
# Centered on XY plane, sitting on Z=0
main_body = cq.Workplane("XY").box(block_length, block_width, block_height)

# Create the top holes
# We select the top face, then create two points for the holes
main_body = (
    main_body.faces(">Z")
    .workplane()
    .pushPoints([(-hole_x_offset, hole_y_offset), (hole_x_offset, hole_y_offset)])
    .hole(hole_diameter)
)

# Function to create a single hooked leg
def create_hook_leg(loc):
    # Draw the profile of the hook leg on the XZ plane (side view)
    # The profile looks like a rectangle with a triangle/chamfer at the bottom
    
    # Points for a hook profile facing outwards or inwards. 
    # Based on the image, the hooks seem to point outward relative to the center of the block.
    # Let's create a generic hook profile on the XZ plane.
    
    # Define the 2D shape of the leg with hook
    pts = [
        (0, 0),
        (foot_width, 0),
        (foot_width, -foot_height + foot_hook_height), # Start of hook taper
        (foot_width + foot_hook_size, -foot_height),   # Tip of hook
        (0, -foot_height),
        (0, 0)
    ]
    
    # Based on the image, the legs are thin in the Y direction (foot_depth)
    # and wide in the X direction (foot_width).
    # Wait, looking closer at the image, the legs are flat tabs.
    # The hooks point outward along the Y axis.
    # Let's re-evaluate orientation.
    # The legs are on the bottom face (>Z).
    # They are aligned along the long edges.
    
    # Let's build them differently. Let's sketch on the YZ plane for the side profile?
    # Actually, sketching on the bottom face and extruding is easiest for the straight part,
    # but the hook shape is an undercut.
    
    # Strategy: Create the L-shape/Hook profile and extrude it.
    # The profile is in the YZ plane (width/height) mostly.
    
    return (
        cq.Workplane("YZ")
        .polyline([
            (0, 0),
            (0, -foot_height),
            (foot_hook_size, -foot_height), # The hook tip
            (0, -foot_height + foot_hook_height), # The angle back
            (0, 0)
        ])
        .close()
        .extrude(foot_width) # This extrudes in X
    )

# Instead of a complex function, let's just add the legs to the bottom face directly using boolean operations.

# Define leg positions relative to the bottom center
leg_x_spacing = block_length * 0.7 # Distance between leg pairs along length
leg_y_spacing = block_width - foot_depth # Distance between leg pairs along width

# Create a single leg geometry to be reused/mirrored
# Profile on the YZ plane (looking from the end of the block)
# The hook points OUTWARD.
leg_profile_pts = [
    (0, 0), # Top inside corner (at bottom of block)
    (foot_depth, 0), # Top outside corner
    (foot_depth, -foot_height + foot_hook_height), # Start of taper
    (foot_depth + foot_hook_size, -foot_height), # Tip of hook
    (0, -foot_height), # Bottom inside corner
    (0, 0) # Close
]

# Create one leg
leg_geo = (
    cq.Workplane("YZ")
    .polyline(leg_profile_pts)
    .close()
    .extrude(foot_width/2.0) # Extrude half width in +X
    .union(
        cq.Workplane("YZ")
        .polyline(leg_profile_pts)
        .close()
        .extrude(-foot_width/2.0) # Extrude half width in -X
    )
)

# Position legs
# 1. Front Left (when looking at the image)
# X is roughly at -block_length/4 and +block_length/4
# Y is at the edges (-block_width/2, +block_width/2)

x_positions = [-block_length/2.0 + 5.0, block_length/2.0 - 5.0]
y_offset = block_width/2.0 - foot_depth # Adjust so outer face is flush

# We need to orient the hook outwards.
# The `leg_geo` created above has the flat back at X=0.
# The hook points in +Y.

final_legs = cq.Assembly()

for x in x_positions:
    # Front side (Y is negative in standard view, but let's assume image perspective)
    # Let's assume standard XY:
    # Side 1 (Positive Y)
    final_legs.add(
        leg_geo
        .translate((x, y_offset, -block_height/2.0)),
        name=f"leg_pos_{x}"
    )
    
    # Side 2 (Negative Y)
    # We need to mirror or rotate the leg profile so the hook points to -Y
    final_legs.add(
        leg_geo
        .rotate((0,0,0), (0,0,1), 180) # Rotate around Z to flip Y direction
        .translate((x, -y_offset, -block_height/2.0)),
        name=f"leg_neg_{x}"
    )

# Combine body and legs
result = main_body.union(final_legs.toCompound())

# Center the result on the origin for better viewing
result = result.translate((0, 0, block_height/2.0))