import cadquery as cq

# --- Parametric Dimensions ---
track_width = 40.0
track_thickness = 1.0

# Ramp dimensions
ramp_start_length = 100.0  # Length of the straight part before curve
ramp_radius = 50.0         # Radius of the curved transition
ramp_height = 30.0         # Total vertical rise of the curved part
ramp_angle = 45.0          # Angle of the final slope (approximate based on visuals)

# Support Structure Dimensions
support_post_thickness = 2.0
support_base_width = track_width + 4.0 # Slightly wider than track
support_height = 40.0 # Height of the tallest posts

# --- Geometry Construction ---

# 1. Create the Track (The main surface)
# We will create a path in the XZ plane and sweep a rectangle along it.

# Define points for the path
p0 = (0, 0)
p1 = (ramp_start_length, 0)

# We need a curved path. We'll use a spline or an arc. 
# Looking at the image, it goes straight flat, then curves up.
# Let's model the path using a sketch or a wire.

# Create the profile to sweep
profile = cq.Workplane("YZ").rect(track_thickness, track_width)

# Create the path
# Start at origin, go straight along X, then tangent arc up to a point
path = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(ramp_start_length, 0)
    .tangentArcPoint((ramp_start_length + ramp_radius, ramp_radius))
)

# Sweep the profile along the path
track = (
    cq.Workplane("XY") # This workplane is just a reference, the sweep uses the path
    .rect(track_width, track_thickness) # Initial cross section
    .sweep(path, isFrenet=True)
)

# 2. Create the Support Structure
# The support is at the end of the curve.
# It looks like a frame made of thin square beams.

# Calculate the position of the support
support_x = ramp_start_length + ramp_radius
support_y = 0 # Center
support_z = 0 # Base level

# Let's build the frame using simple boxes relative to the end of the track.
# The track end is roughly at (ramp_start_length + ramp_radius, 0, ramp_radius).
# Wait, the tangent arc in CadQuery is relative. Let's adjust logic.
# The path ends at X = ramp_start_length + ramp_radius, Z = ramp_radius.

support_center_x = ramp_start_length + ramp_radius - 5.0 # Slightly back from the very tip
support_base_z = 0.0
top_z = ramp_radius  # Height of the track at that point

# Create vertical posts
post_height = top_z
post_dist_x = 15.0 # Distance between front and back posts of the support tower

# Function to make a simple post
def make_post(h):
    return cq.Workplane("XY").box(support_post_thickness, support_post_thickness, h)

# Front posts (taller side, where track is highest)
post_fl = make_post(post_height).translate((support_center_x, track_width/2, post_height/2))
post_fr = make_post(post_height).translate((support_center_x, -track_width/2, post_height/2))

# Back posts (shorter side, further down the X axis or "inside" the curve slightly?)
# The image shows a triangular truss structure. Let's approximate the frame.
# It looks like two A-frames or H-frames connected.
# Let's simplify: 4 posts, cross beams.

# Adjust positions to match the visual "tower" at the end
tower_x = ramp_start_length + ramp_radius
tower_h = ramp_radius

# Vertical Posts
v_post_1 = cq.Workplane("XY").box(support_post_thickness, support_post_thickness, tower_h).translate((tower_x, track_width/2, tower_h/2))
v_post_2 = cq.Workplane("XY").box(support_post_thickness, support_post_thickness, tower_h).translate((tower_x, -track_width/2, tower_h/2))

# Horizontal Beams (connecting posts L-R)
h_beam_top = cq.Workplane("XY").box(support_post_thickness, track_width, support_post_thickness).translate((tower_x, 0, tower_h))
h_beam_mid = cq.Workplane("XY").box(support_post_thickness, track_width, support_post_thickness).translate((tower_x, 0, tower_h/2))

# Diagonal/Support legs going backwards
# Looking at the image, there's a structure supporting the curve.
# Let's add a second set of shorter posts "behind" (negative X direction relative to tower)
back_offset = 20.0
back_h = tower_h * 0.6 # Shorter

v_post_3 = cq.Workplane("XY").box(support_post_thickness, support_post_thickness, back_h).translate((tower_x - back_offset, track_width/2, back_h/2))
v_post_4 = cq.Workplane("XY").box(support_post_thickness, support_post_thickness, back_h).translate((tower_x - back_offset, -track_width/2, back_h/2))

# Connecting front to back
c_beam_1 = cq.Workplane("XY").box(back_offset, support_post_thickness, support_post_thickness).translate((tower_x - back_offset/2, track_width/2, back_h))
c_beam_2 = cq.Workplane("XY").box(back_offset, support_post_thickness, support_post_thickness).translate((tower_x - back_offset/2, -track_width/2, back_h))

# Diagonal braces (simple lines for visual similarity)
diag_len = (back_offset**2 + (tower_h - back_h)**2)**0.5
diag_angle = 30 # Approximation

# Combine support structure
support_structure = (
    v_post_1.union(v_post_2)
    .union(h_beam_top).union(h_beam_mid)
    .union(v_post_3).union(v_post_4)
    .union(c_beam_1).union(c_beam_2)
)

# Rotate support slightly to match the end of the arc if strictly perpendicular,
# but usually these are vertical relative to ground. The current setup is vertical.

# 3. Combine Geometry
# The sweep might result in a solid that needs to be properly oriented.
# The initial rect was in XY plane swept along XZ path.
# Orientation depends on how the sweep interprets the profile normal.

# Re-doing the sweep with explicit orientation to ensure flat ribbon style
# We create a solid ribbon by extruding a wire or thickening a surface,
# or sweeping a thin rectangle.
# Let's try the sweep again but simpler:
path_wire = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(ramp_start_length, 0)
    .tangentArcPoint((ramp_start_length + ramp_radius, ramp_radius))
)

# Create a profile perpendicular to the start of the path
# Path starts along X, so profile should be in YZ
profile_sketch = cq.Workplane("YZ").rect(track_thickness, track_width)

track_solid = (
    cq.Workplane("YZ")
    .rect(track_thickness, track_width) # Profile
    .sweep(path_wire, isFrenet=True) # Sweep
)

# Color separation logic (simulated by splitting geometry if needed, but here just a single solid)
# The image shows a black section (flat) and a grey section (curved/support).
# We can model them separately if needed, but a single union is standard for CAD export.

# Combine track and support
result = track_solid.union(support_structure)

# Position adjustments if necessary to match the isometric view roughly
# (CadQuery usually centers things, but our construction started at 0,0,0)