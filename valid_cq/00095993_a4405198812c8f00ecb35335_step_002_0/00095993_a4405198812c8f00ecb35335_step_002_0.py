import cadquery as cq

# Overall dimensions of the block
block_width = 30.0
block_depth = 30.0
block_height = 80.0

# Dimensions for the bowtie/butterfly pocket on the top face
pocket_depth = 12.0
top_outer_width = 22.0    # Width across the widest part of the wings
top_outer_height = 16.0   # Height of the wings
waist_width = 4.0         # Horizontal gap at the center restriction
waist_height = 4.0        # Vertical thickness of the center restriction

# Taper factor for the bottom of the pocket (simulating draft angle)
scale_factor = 0.65

def get_bowtie_profile(w, h, ww, wh):
    """
    Generates a list of (x,y) tuples defining a bowtie shape centered at (0,0).
    w, h: Outer width and height
    ww, wh: Waist width and height
    """
    return [
        (-w/2, -h/2),    # Bottom-left corner
        (-w/2, h/2),     # Top-left corner
        (-ww/2, wh/2),   # Waist top-left
        (ww/2, wh/2),    # Waist top-right
        (w/2, h/2),      # Top-right corner
        (w/2, -h/2),     # Bottom-right corner
        (ww/2, -wh/2),   # Waist bottom-right
        (-ww/2, -wh/2)   # Waist bottom-left
    ]

# Generate profile points for top and bottom of the pocket
top_pts = get_bowtie_profile(top_outer_width, top_outer_height, waist_width, waist_height)
bot_pts = get_bowtie_profile(top_outer_width * scale_factor, 
                             top_outer_height * scale_factor, 
                             waist_width * scale_factor, 
                             waist_height * scale_factor)

# Create the base block
result = cq.Workplane("XY").box(block_width, block_depth, block_height)

# Create the lofted cut on the top face
result = (
    result.faces(">Z").workplane()      # Workplane on the top face
    .polyline(top_pts).close()          # Sketch the top profile
    .workplane(offset=-pocket_depth)    # Create a new workplane at pocket depth
    .polyline(bot_pts).close()          # Sketch the smaller bottom profile
    .loft(combine="cut")                # Loft between the two profiles and cut
)