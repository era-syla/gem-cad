import cadquery as cq

# ==========================================
# Parameters & Dimensions
# ==========================================
frame_height = 2400.0
frame_width_long = 3000.0  # Distance to right post
frame_width_short = 1800.0 # Distance to front-left post

# Profile specs (approx. 60mm square extrusion)
profile_size = 60.0
profile_wall = 4.0

# Base Plate specs
base_size = 120.0
base_thick = 10.0
hole_dia = 12.0
hole_spacing = 90.0

# Gusset specs
gusset_leg = 250.0
gusset_thick = 6.0

# ==========================================
# Geometry Generators
# ==========================================

# 1. Base Plate
# ------------------------------------------
base_plate = (
    cq.Workplane("XY")
    .box(base_size, base_size, base_thick)
    .faces(">Z").workplane()
    .rect(hole_spacing, hole_spacing, forConstruction=True)
    .vertices()
    .hole(hole_dia)
)

# 2. Vertical Posts
# ------------------------------------------
# The vertical posts sit on the base plate.
# The horizontal top frame sits on top of the posts.
post_len = frame_height - profile_size - base_thick

def make_profile_extrusion(length):
    return (
        cq.Workplane("XY")
        .rect(profile_size, profile_size)
        .rect(profile_size - 2*profile_wall, profile_size - 2*profile_wall)
        .extrude(length)
    )

post_geo = make_profile_extrusion(post_len)

# 3. Top Horizontal Frame (L-shaped sweep)
# ------------------------------------------
# We create the L-shaped top frame as a single sweep to get the mitered corner automatically.
# Path: From (0, frame_width_short) -> (0, 0) -> (frame_width_long, 0)
# This corresponds to: Front-Left -> Back-Left (Corner) -> Back-Right

sweep_path = (
    cq.Workplane("XY")
    .moveTo(0, frame_width_short)
    .lineTo(0, 0)
    .lineTo(frame_width_long, 0)
)

# The profile for the sweep must be defined on the plane perpendicular to the start of the path.
# Path starts at (0, y) moving -Y towards origin. Normal plane is XZ.
top_profile_sketch = (
    cq.Workplane("XZ")
    .rect(profile_size, profile_size)
    .rect(profile_size - 2*profile_wall, profile_size - 2*profile_wall)
)

# Sweep and position at correct height
# Sweep center Z is at 0, need to move to frame_height - profile_size/2
beam_z_center = frame_height - (profile_size / 2.0)
top_frame = top_profile_sketch.sweep(sweep_path).translate((0, 0, beam_z_center))

# 4. Gussets
# ------------------------------------------
# Triangular stiffeners at the corners.
# Defined relative to the inner corner point between post and beam.
# Z reference is the bottom face of the top beam.
z_gusset_ref = frame_height - profile_size
offset = profile_size / 2.0 # Start from face of profile

# Gusset 1: Corner Post -> Long Beam (+X)
g1 = (
    cq.Workplane("XZ")
    .polyline([
        (offset, z_gusset_ref), 
        (offset + gusset_leg, z_gusset_ref), 
        (offset, z_gusset_ref - gusset_leg)
    ])
    .close()
    .extrude(gusset_thick)
    .translate((0, -gusset_thick/2, 0)) # Center on profile axis
)

# Gusset 2: Corner Post -> Short Beam (+Y)
g2 = (
    cq.Workplane("YZ")
    .polyline([
        (offset, z_gusset_ref), 
        (offset + gusset_leg, z_gusset_ref), 
        (offset, z_gusset_ref - gusset_leg)
    ])
    .close()
    .extrude(gusset_thick)
    .translate((-gusset_thick/2, 0, 0))
)

# Gusset 3: Right Post -> Long Beam (-X direction)
g3 = (
    cq.Workplane("XZ")
    .polyline([
        (frame_width_long - offset, z_gusset_ref), 
        (frame_width_long - offset - gusset_leg, z_gusset_ref), 
        (frame_width_long - offset, z_gusset_ref - gusset_leg)
    ])
    .close()
    .extrude(gusset_thick)
    .translate((0, -gusset_thick/2, 0))
)

# Gusset 4: Front Post -> Short Beam (-Y direction)
g4 = (
    cq.Workplane("YZ")
    .polyline([
        (frame_width_short - offset, z_gusset_ref), 
        (frame_width_short - offset - gusset_leg, z_gusset_ref), 
        (frame_width_short - offset, z_gusset_ref - gusset_leg)
    ])
    .close()
    .extrude(gusset_thick)
    .translate((-gusset_thick/2, 0, 0))
)

# ==========================================
# Assembly
# ==========================================

# Positions
pos_corner = (0, 0)
pos_right  = (frame_width_long, 0)
pos_front  = (0, frame_width_short)

# Vertical offset for posts (start on top of base plate)
z_post_start = base_thick

# Create Instances
p1 = post_geo.translate((pos_corner[0], pos_corner[1], z_post_start))
p2 = post_geo.translate((pos_right[0], pos_right[1], z_post_start))
p3 = post_geo.translate((pos_front[0], pos_front[1], z_post_start))

# Bases (centered Z)
b1 = base_plate.translate((pos_corner[0], pos_corner[1], base_thick/2))
b2 = base_plate.translate((pos_right[0], pos_right[1], base_thick/2))
b3 = base_plate.translate((pos_front[0], pos_front[1], base_thick/2))

# Combine all solids
result = (
    p1.union(p2).union(p3)
    .union(b1).union(b2).union(b3)
    .union(top_frame)
    .union(g1).union(g2).union(g3).union(g4)
)