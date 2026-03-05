import cadquery as cq

# ==========================================
# Parameters & Dimensions
# ==========================================

# Overall dimensions
stand_height = 850.0
stand_width = 950.0    # Length of the top beam
foot_length = 500.0    # Length of the base feet

# Component profiles (Width x Height/Depth)
# Posts (Uprights)
post_thick = 40.0      # Dimension along X
post_depth = 80.0      # Dimension along Y

# Feet
foot_height = 80.0
foot_thick = 40.0
foot_chamfer = 30.0    # Chamfer size on top corners
foot_arch_w = 240.0    # Width of bottom cutout
foot_arch_h = 15.0     # Height of bottom cutout

# Top Beam
top_beam_height = 100.0
top_beam_thick = 40.0  # Y dimension

# Crossbeam (Lower support)
cross_height = 70.0
cross_thick = 25.0
cross_elevation = 320.0 # Height from ground to center of crossbeam
cross_overhang = 25.0   # Tenon protrusion beyond post

# Layout
post_spacing = 650.0   # Center-to-center distance between posts

# ==========================================
# Component Builders
# ==========================================

def create_foot():
    """
    Creates the foot profile on the YZ plane and extrudes in X.
    The foot has chamfered top corners and a relief cut at the bottom.
    """
    L, H = foot_length, foot_height
    c = foot_chamfer
    aw, ah = foot_arch_w, foot_arch_h
    
    # Trace the profile starting from bottom-left corner
    # Note: Points are defined in YZ plane coordinates (Y, Z)
    pts = [
        (-L/2.0, 0),             # Bottom left outer
        (-aw/2.0, 0),            # Start of arch
        (-aw/2.0 + ah, ah),      # Arch inner left (angled)
        (aw/2.0 - ah, ah),       # Arch inner right (angled)
        (aw/2.0, 0),             # End of arch
        (L/2.0, 0),              # Bottom right outer
        (L/2.0, H - c),          # Start of chamfer right
        (L/2.0 - c, H),          # End of chamfer right
        (-L/2.0 + c, H),         # Start of chamfer left
        (-L/2.0, H - c)          # End of chamfer left
    ]
    
    # Extrude symmetrically in X direction
    return cq.Workplane("YZ").polyline(pts).close().extrude(foot_thick/2.0, both=True)

def create_post():
    """
    Creates a vertical post.
    Height is calculated to fit between foot and top beam.
    """
    # Calculate post height relative to other components
    h_post = stand_height - foot_height - top_beam_height
    
    # Create rectangular prism
    return (cq.Workplane("XY")
            .rect(post_thick, post_depth)
            .extrude(h_post)
            )

def create_top_beam():
    """
    Creates the horizontal top beam.
    """
    return (cq.Workplane("YZ")
            .rect(top_beam_thick, top_beam_height)
            .extrude(stand_width/2.0, both=True)
            )

def create_crossbeam():
    """
    Creates the lower crossbeam.
    Length includes the span between posts plus overhangs.
    """
    total_len = post_spacing + post_thick + (2 * cross_overhang)
    
    return (cq.Workplane("YZ")
            .rect(cross_thick, cross_height)
            .extrude(total_len/2.0, both=True)
            )

# ==========================================
# Assembly
# ==========================================

# 1. Instantiate Geometry
foot_shape = create_foot()
post_shape = create_post()
top_beam_shape = create_top_beam()
crossbeam_shape = create_crossbeam()

# 2. Position and Combine Parts

# Feet
# Positioned at +/- half the post spacing
foot_left = foot_shape.translate((-post_spacing/2.0, 0, 0))
foot_right = foot_shape.translate((post_spacing/2.0, 0, 0))

# Posts
# Sit on top of the feet (Z = foot_height)
post_z_pos = foot_height
post_left = post_shape.translate((-post_spacing/2.0, 0, post_z_pos))
post_right = post_shape.translate((post_spacing/2.0, 0, post_z_pos))

# Top Beam
# Sits on top of the posts
# Z center of beam = (Top of post) + (Half beam height)
# Top of post = stand_height - top_beam_height
top_beam_z_center = (stand_height - top_beam_height) + (top_beam_height / 2.0)
top_beam = top_beam_shape.translate((0, 0, top_beam_z_center))

# Crossbeam
# Positioned at specified elevation
crossbeam = crossbeam_shape.translate((0, 0, cross_elevation))

# 3. Create Final Solid
result = (foot_left
          .union(foot_right)
          .union(post_left)
          .union(post_right)
          .union(top_beam)
          .union(crossbeam)
          )