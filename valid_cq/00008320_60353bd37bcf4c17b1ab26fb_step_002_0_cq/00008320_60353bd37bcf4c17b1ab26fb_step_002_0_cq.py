import cadquery as cq

# --- Parametric Dimensions ---
# Base dimensions
base_width = 300.0   # Total width of the base (between feet)
base_depth = 150.0   # Length of the feet
base_height = 30.0   # Height of the main base blocks
beam_thickness = 30.0 # Thickness of the horizontal connector

# Vertical Posts
post_height = 600.0
post_width = 15.0
post_depth = 15.0

# Top Bar
top_bar_length = base_width + 100.0 # Extend slightly past posts
top_bar_width = 15.0
top_bar_depth = 25.0
top_bar_offset = 50.0 # How far down from the top of the post

# Triangular Supports
support_height = 150.0
support_width = 10.0
support_thickness = 10.0
support_spread = 60.0 # Width at the base of the triangle

# --- Geometry Construction ---

# 1. Base Structure
# We'll create the left foot, right foot, and the connecting beam.

# Left Foot (Consists of two blocks with a gap or a single block with a slot?) 
# Looking at the image, the base feet look like rectangular blocks. 
# There is a connecting beam running between them.
foot_dims = (beam_thickness + 40, base_depth, base_height) # Width, Depth, Height

# Create a single foot
foot = cq.Workplane("XY").box(foot_dims[0], foot_dims[1], foot_dims[2])

# Left Foot placement
left_foot = foot.translate((-base_width/2, 0, base_height/2))

# Right Foot placement
right_foot = foot.translate((base_width/2, 0, base_height/2))

# Connecting Beam (between feet)
# It seems to sit on top of the feet or join them. 
# In the image, there is a central bar connecting the two heavy bases.
# It looks like it sits at the bottom level. Let's make it connect the centers.
connector = cq.Workplane("XY").box(base_width, beam_thickness, beam_thickness) \
    .translate((0, 0, beam_thickness/2))

# 2. Vertical Posts
# Two tall thin posts rising from the center of the feet.
post = cq.Workplane("XY").box(post_width, post_depth, post_height)
left_post = post.translate((-base_width/2, 0, post_height/2 + base_height))
right_post = post.translate((base_width/2, 0, post_height/2 + base_height))

# 3. Top Horizontal Bar
# Connects the two posts near the top.
top_bar = cq.Workplane("XY").box(top_bar_length, top_bar_depth, top_bar_width) # Note dimensions orientation
# Position: centered X, Y, and near top of Z
top_bar_z = base_height + post_height - top_bar_offset
top_bar_obj = top_bar.translate((0, 0, top_bar_z))

# 4. Triangular Supports (Gussets)
# Located at the base of the left post.
# It looks like an inverted 'V' shape made of two angled struts.

def create_angled_strut(angle_degrees, height, thickness, x_offset):
    # Create a strut angled towards the post
    # Length calculation based on height and angle
    # Simplified approach: Create a box, rotate it, cut bottom and side
    
    # Let's define the triangle points on the XZ plane
    # Peak point on the post
    p1 = (-base_width/2, height + base_height)
    # Base point on the foot (offset from center)
    p2 = (-base_width/2 - x_offset, base_height)
    
    # Construct a path or loft? 
    # Let's simply make a box and rotate it for simplicity, 
    # or build a polygon and extrude.
    
    path_pts = [
        (-base_width/2 - thickness/2, height + base_height),
        (-base_width/2 + thickness/2, height + base_height),
        (-base_width/2 + thickness/2 - x_offset, base_height),
        (-base_width/2 - thickness/2 - x_offset, base_height)
    ]
    
    # This creates a solid shape for the strut
    strut = (cq.Workplane("XZ")
             .polyline(path_pts)
             .close()
             .extrude(thickness/2) # Extrude half thickness both ways? No, specific depth.
             )
    
    # Center the extrusion on Y=0
    strut = strut.translate((0, -thickness/4, 0)) # Initial position
    # The image shows two struts forming a triangle. 
    # One goes forward (positive Y), one goes backward (negative Y)?
    # No, looking at the image, the triangle is in the Plane of the frame (XZ plane).
    # Wait, looking closer at the crop, the supports are on the SIDE of the post, 
    # angling out along the Y-axis (depth) or the X-axis (width)?
    # The supports are on the left post. They splay out along the Y-axis (depth).
    
    return strut

# Let's rebuild the support strategy based on the visual "A" frame shape on the left side.
# It connects the vertical post to the base foot along the Depth (Y axis).
# One strut goes from post (high) to front of foot.
# One strut goes from post (high) to back of foot.

support_peak_z = base_height + support_height
support_base_y_offset = base_depth / 2 - 10

# Create points for a loft or a hull
# Top point at the post
top_pt = cq.Vector(-base_width/2, 0, support_peak_z)
# Front base point
front_pt = cq.Vector(-base_width/2, -support_base_y_offset, base_height)
# Back base point
back_pt = cq.Vector(-base_width/2, support_base_y_offset, base_height)

# Create Front Strut
# We use a helper function to make a stick between two points
def make_strut(p1, p2, w, t):
    length = (p1 - p2).Length
    center = (p1 + p2) / 2
    
    # Calculate angle
    # Vector direction
    v = p2 - p1
    # Simple box rotated
    # Angle relative to Z axis in YZ plane
    import math
    angle = math.degrees(math.atan2(v.y, v.z))
    
    return (cq.Workplane("YZ")
            .box(t, length, w)
            .rotate((0,0,0), (1,0,0), angle)
            .translate((center.x, center.y, center.z))
            )

front_strut = make_strut(top_pt, front_pt, support_width, support_thickness)
back_strut = make_strut(top_pt, back_pt, support_width, support_thickness)

# Add a small block at the peak where they join if needed, 
# but the overlap with the post should handle it.

# --- Combine All Parts ---

result = (left_foot
          .union(right_foot)
          .union(connector)
          .union(left_post)
          .union(right_post)
          .union(top_bar_obj)
          .union(front_strut)
          .union(back_strut)
          )