import cadquery as cq

# --- Parameter Definitions ---
# Overall dimensions of the base frame
frame_length = 60.0  # Long side (X)
frame_width = 30.0   # Short side (Y)
frame_height = 5.0   # Thickness of the base (Z)
frame_thickness = 5.0 # Width of the frame material

# Vertical post dimensions
post_height = 15.0   # Height from the top of the base
post_width = 4.0     # X dimension of the post
post_depth = 4.0     # Y dimension of the post (matches frame thickness roughly)

# Snap hook dimensions
hook_overhang = 2.0  # How much the hook sticks out
hook_tip_height = 4.0 # Height of the tapered part
hook_flat_top = 2.0  # Length of the flat top section (if any, appears pointed but slightly flat)

# --- Geometry Construction ---

# 1. Create the base rectangular frame
# We create a solid box and then cut out the center
base_outer = cq.Workplane("XY").box(frame_length, frame_width, frame_height)
base_inner = cq.Workplane("XY").box(frame_length - 2*frame_thickness, 
                                    frame_width - 2*frame_thickness, 
                                    frame_height)
base_frame = base_outer.cut(base_inner)

# 2. Define the positions for the vertical posts
# There are 4 corners, each having 2 posts near it, but looking closely:
# It looks like pairs of posts on the long sides.
# Let's group them: two pairs on the positive Y side, two pairs on the negative Y side.
# Actually, looking at the image:
# - There are 4 corner clusters.
# - Each cluster has two posts.
# - Wait, let's look closer.
# - On the near long edge: 2 posts on the left, 2 posts on the right.
# - On the far long edge: 2 posts on the left, 2 posts on the right.
# - However, the "hooks" are only on specific posts.
# - The posts are located on the long edges (X-aligned), inset slightly from the corners.

# Let's define offsets for the posts relative to the center
# x_offset_outer: Distance from center to the outer post of a pair
# x_offset_inner: Distance from center to the inner post of a pair
# y_offset: Distance from center to the centerline of the long frame edge

y_offset = (frame_width - frame_thickness) / 2
x_spacing = 8.0 # Gap between the two posts in a pair
x_group_offset = (frame_length/2) - frame_thickness - (post_width/2) 
# x_group_offset puts the outer post flush with the inner corner, roughly.
# Let's adjust slightly to look like the image.
x_outer_pos = (frame_length / 2) - 5.0
x_inner_pos = x_outer_pos - x_spacing

# Locations for the 8 basic posts
# (x, y) tuples
post_locations = [
    (x_outer_pos, y_offset), (x_inner_pos, y_offset),   # Top Right
    (-x_outer_pos, y_offset), (-x_inner_pos, y_offset), # Top Left
    (x_outer_pos, -y_offset), (x_inner_pos, -y_offset), # Bottom Right
    (-x_outer_pos, -y_offset), (-x_inner_pos, -y_offset)# Bottom Left
]

# 3. Create the basic posts
# We start drawing on the top face of the base frame
posts = (
    base_frame.faces(">Z").workplane()
    .pushPoints(post_locations)
    .rect(post_width, post_depth)
    .extrude(post_height)
)

# 4. Add the Snap Hooks
# Looking at the image, the hooks are on the *inner* posts of the pairs on the short ends?
# No, looking carefully:
# There are two hooks on the far left side (one on the near edge, one on the far edge).
# There are two hooks on the far right side (one on the near edge, one on the far edge).
# Specifically, the hooks are on the posts closest to the middle of the long edges (the "inner" posts).
# And the hooks point INWARDS towards the center of the frame (along X axis).

# Identifying the "inner" posts based on our coordinates:
# (x_inner_pos, y_offset), (-x_inner_pos, y_offset), (x_inner_pos, -y_offset), (-x_inner_pos, -y_offset)
# Hooks point towards x=0.

# Let's build the hook profile. It's a triangle added to the side.
# We need to select the specific faces of the specific posts.
# This can be tricky with selectors. It's often easier to just build the hook geometry and union it.

def create_hook(loc, direction):
    """
    Creates a hook solid at a specific (x,y) location.
    direction: 1 for pointing +X, -1 for pointing -X
    """
    x, y = loc
    # The hook is at the top of the post.
    # We draw on the side face of the post.
    
    # Calculate center of the post at top height
    z_start = frame_height + post_height
    
    # We want to draw on the XZ plane essentially, but located at y
    # Orientation depends on direction.
    
    hook_shape = (
        cq.Workplane("XZ")
        .workplane(offset=-y) # Shift to the post's Y position (note coordinate system flip potential)
        .center(x, z_start)   # Move origin to top center of post
    )
    
    # If we are at +y (back), normal is towards front. If -y, normal is towards back.
    # Using global XZ plane and offsetting Y is consistent.
    
    # Draw the triangle profile
    # Local coordinates: X is global X, Y is global Z
    # We start at the edge of the post.
    # Post width extends from x - width/2 to x + width/2
    
    edge_x = -direction * (post_width / 2) # The face towards the center
    
    pts = [
        (edge_x, 0),  # Top inner corner of post
        (edge_x + (-direction * hook_overhang), -hook_tip_height), # Tip of hook
        (edge_x, -hook_tip_height) # Point on post surface
    ]
    
    # We need to ensure the hook has thickness (Y direction)
    # The default extrusion for XZ plane is in global Y.
    # Since we offset by -y, we are on the centerline.
    # We need to extrude symmetrically or by thickness.
    
    # Let's try a different approach: Build on the face of the post.
    
    # Find the post face. 
    # If direction is -1 (pointing left, so post is on right), we want the -X face.
    # If direction is 1 (pointing right, so post is on left), we want the +X face.
    
    face_dir = "<X" if direction == 1 else ">X"
    
    # To select the specific post, we filter by the center point
    post_filter = posts.faces(face_dir).filter(lambda f: abs(f.Center().x - (x + direction*post_width/2)) < 0.1 and abs(f.Center().y - y) < 0.1)
    
    # Draw hook wedge
    # We draw a triangle on the side face and extrude
    try:
        hook = (
            post_filter.workplane(centerOption="CenterOfMass")
            .polyline([(0, 0), (hook_overhang, -hook_tip_height), (0, -hook_tip_height)])
            .close()
            .extrude(post_depth) # This might extrude the wrong way depending on face normal
        )
        return hook
    except:
        # Fallback if selection fails (though coordinate math usually safer)
        return None


# Re-evaluating the image for hook placement:
# The hooks are on the "inner" posts.
# Left side inner posts: x = -x_inner_pos. Hook points RIGHT (+X).
# Right side inner posts: x = x_inner_pos. Hook points LEFT (-X).

# Let's construct the wedges manually and union them, it's more robust than selectors for multiple similar objects.
hooks = []

# Left side hooks (at -x, pointing +X)
for y_pos in [y_offset, -y_offset]:
    x_pos = -x_inner_pos
    
    # Define wedge points in XZ plane
    pts = [
        (0, 0), 
        (hook_overhang, -hook_tip_height), 
        (0, -hook_tip_height)
    ]
    
    wedge = (
        cq.Workplane("XZ")
        .polyline(pts).close()
        .extrude(post_depth) # Extrudes in Y
    )
    
    # Move wedge to correct position
    # The wedge origin (0,0) needs to be at the top-inner corner of the post
    # X: x_pos + post_width/2 (since x_pos is center, and we want +X face)
    # Y: Centered at y_pos
    # Z: frame_height + post_height
    
    wedge = wedge.translate((x_pos + post_width/2, -post_depth/2, frame_height + post_height))
    # Correct Y translation: Extrude centers on the plane? No, usually normal.
    # Workplane("XZ") creates plane at Y=0. Extrude(d) goes to Y=d.
    # So initial Y range is 0 to post_depth.
    # We want it centered at y_pos.
    # So translate Y by (y_pos - post_depth/2).
    
    wedge = wedge.translate((0, y_pos, 0))
    hooks.append(wedge)

# Right side hooks (at +x, pointing -X)
for y_pos in [y_offset, -y_offset]:
    x_pos = x_inner_pos
    
    # Define wedge points - flipped X
    pts = [
        (0, 0), 
        (-hook_overhang, -hook_tip_height), 
        (0, -hook_tip_height)
    ]
    
    wedge = (
        cq.Workplane("XZ")
        .polyline(pts).close()
        .extrude(post_depth)
    )
    
    # Move wedge
    # Origin at top-inner corner (facing center)
    # X: x_pos - post_width/2
    wedge = wedge.translate((x_pos - post_width/2, -post_depth/2, frame_height + post_height))
    wedge = wedge.translate((0, y_pos, 0))
    hooks.append(wedge)

# 5. Combine everything
result = posts
for h in hooks:
    result = result.union(h)

# 6. Optional: Fillets/Chamfers to match the "molded" look (not explicitly requested but good practice)
# The image shows fairly sharp edges, maybe small fillets on the frame inner corners.
# Let's leave it sharp to strictly follow the "blocky" geometry shown.

# Final Export
# result is already defined.