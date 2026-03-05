import cadquery as cq

# Parametric dimensions
tube_radius = 10.0      # Radius of the tube cross-section
handle_height = 400.0   # Total vertical height (approximate)
handle_width = 80.0     # Width between the vertical legs
gap_width = 20.0        # Gap between the top opposing ends
bend_radius = 20.0      # Radius of the bends

# Calculate path points
# We will create a path that starts at the top left, goes down, across, up, and inwards
# Coordinates relative to an origin near the bottom center

# Define points for the path
# Let's trace it: Top Left End -> Down -> Right -> Up -> Top Right End

# Start at the top left facing end
p_start = (-handle_width/2 + bend_radius, handle_height, 0)

# Path definition
path = (
    cq.Workplane("XY")
    .moveTo(p_start[0], p_start[1])
    # Short straight inward segment at the top left? No, let's assume it's just a bend.
    # Actually, looking closely, there are small straight sections pointing inwards at the top.
    # Let's model it as a U-shape with inward bends at the top.
    
    # Let's try a different approach: define the centerline points
    # 1. Top Left Tip
    # 2. Top Left Corner (start of vertical)
    # 3. Bottom Left Corner
    # 4. Bottom Right Corner
    # 5. Top Right Corner (start of vertical)
    # 6. Top Right Tip
)

# Refined Dimensions
vertical_length = handle_height - 2 * bend_radius
horizontal_length = handle_width - 2 * bend_radius
inward_length = 20.0 # Length of the straight bit pointing inwards at the top

# Create the path using a wire
# We will start from the top-left tip
path = (
    cq.Workplane("YZ")
    .moveTo(0, handle_height) # Top of left leg
    .lineTo(0, bend_radius)   # Bottom of left leg
    
    # Bottom Left Bend (90 deg)
    .tangentArcPoint((bend_radius, 0)) 
    
    # Bottom Horizontal
    .lineTo(handle_width - bend_radius, 0)
    
    # Bottom Right Bend (90 deg)
    .tangentArcPoint((handle_width, bend_radius))
    
    # Right Vertical Leg
    .lineTo(handle_width, handle_height)
    
    # Top Right Bend (90 deg inwards)
    # The image shows the ends pointing towards each other.
    # We are currently in the YZ plane. Z is up, Y is right.
    # We need to bend in the X direction? No, the image is a simple loop.
    # It looks like a simple rectangle with rounded corners, but open at the top.
    # Wait, looking at the top: The two ends point towards each other.
    # So the path goes: Up -> Bend Inward -> Gap -> Bend Outward (from other side) -> Down
    
    # Let's re-evaluate the shape.
    # It looks like a "C" shape or "U" shape in the profile.
    # Let's assume the handle lies primarily in the YZ plane (Z up).
    # Left vertical leg at Y=0. Right vertical leg at Y=handle_width.
    
    # Top Left:
    # Starts at Y = gap/2? No, looking at the image, there is a distinct gap between two facing cylinders.
    # It implies the tube bends 90 degrees from vertical to horizontal.
    
)

# Let's restart the path construction more systematically.
# Origin at bottom center.
# Right side:
# 1. Start at top inward tip: (gap_width/2, handle_height)
# 2. Go outward to corner radius start: (handle_width/2 - bend_radius, handle_height)
# 3. Arc down to vertical: (handle_width/2, handle_height - bend_radius)
# 4. Go down to bottom corner radius start: (handle_width/2, bend_radius)
# 5. Arc left to horizontal: (handle_width/2 - bend_radius, 0)
# 6. Go left to center: (0, 0)
# ... and mirror or continue for the left side.

# Let's build the full path in one go.
p_top_right_tip = (gap_width/2, handle_height)
p_top_right_bend_start = (handle_width/2 - bend_radius, handle_height)
p_top_right_vertical_start = (handle_width/2, handle_height - bend_radius)
p_bottom_right_vertical_end = (handle_width/2, bend_radius)
p_bottom_right_bend_end = (handle_width/2 - bend_radius, 0)

p_bottom_left_bend_start = (-handle_width/2 + bend_radius, 0)
p_bottom_left_vertical_start = (-handle_width/2, bend_radius)
p_top_left_vertical_end = (-handle_width/2, handle_height - bend_radius)
p_top_left_bend_end = (-handle_width/2 + bend_radius, handle_height)
p_top_left_tip = (-gap_width/2, handle_height)


# Create the path on the YZ plane (Front view)
# We use spline/polyline or distinct moves.
# Note: tangentArcPoint in CadQuery is relative to current position usually? No, can be absolute.
# Let's use Workplane construction.

path = (
    cq.Workplane("YZ")
    .moveTo(p_top_right_tip[0], p_top_right_tip[1])
    .lineTo(p_top_right_bend_start[0], p_top_right_bend_start[1])
    .radiusArc(p_top_right_vertical_start, -bend_radius) # Bend down
    .lineTo(p_bottom_right_vertical_end[0], p_bottom_right_vertical_end[1])
    .radiusArc(p_bottom_right_bend_end, bend_radius) # Bend left
    .lineTo(p_bottom_left_bend_start[0], p_bottom_left_bend_start[1])
    .radiusArc(p_bottom_left_vertical_start, bend_radius) # Bend up
    .lineTo(p_top_left_vertical_end[0], p_top_left_vertical_end[1])
    .radiusArc(p_top_left_bend_end, -bend_radius) # Bend right/inward
    .lineTo(p_top_left_tip[0], p_top_left_tip[1])
)

# Sweep a circle along this path
result = (
    cq.Workplane("XY")
    .workplane(offset=handle_height) # Move to the plane of the start point
    .moveTo(p_top_right_tip[0], 0)   # Move to start of path (Z is now Y in the path coordinates effectively due to plane orientation, let's just align normally)
    # Actually, simpler method: create profile at start of path
    # The start of the path is at (gap_width/2, handle_height, 0) in global coords if we map YZ plane to Y, Z
    
    # Let's redefine carefully to ensure sweeping works.
    # Path is in YZ plane.
    # Profile needs to be perpendicular to the start of the path.
    # Start of path direction is along +Y (from gap outwards).
    # So profile should be in XZ plane? No, path is in YZ plane.
    # Start segment is horizontal (along Y axis).
    # Profile plane should be XZ plane (normal to Y).
)

# Re-creating the path purely in 3D for clarity
path_wire = (
    cq.Workplane("YZ")
    .moveTo(gap_width/2, handle_height)
    .lineTo(handle_width/2 - bend_radius, handle_height)
    .radiusArc((handle_width/2, handle_height - bend_radius), -bend_radius)
    .lineTo(handle_width/2, bend_radius)
    .radiusArc((handle_width/2 - bend_radius, 0), bend_radius)
    .lineTo(-handle_width/2 + bend_radius, 0)
    .radiusArc((-handle_width/2, bend_radius), bend_radius)
    .lineTo(-handle_width/2, handle_height - bend_radius)
    .radiusArc((-handle_width/2 + bend_radius, handle_height), -bend_radius)
    .lineTo(-gap_width/2, handle_height)
)

# Create the profile to sweep
# The path starts at (gap_width/2, handle_height) in YZ coordinates.
# The tangent at start is (1, 0, 0) in YZ local, which is (0, 1, 0) in global if mapped directly.
# Let's define the profile on a plane perpendicular to the start.
# The start segment goes from right to right-er? 
# Wait, p_top_right_tip is (gap/2). p_top_right_bend_start is (width/2 - rad).
# Since width > gap, we are moving in +Y direction.
# So normal is Y axis. Plane is XZ.
# Center of profile is at (0, gap_width/2, handle_height).
# But Workplane("YZ") puts X axis of local plane as global Y, Y axis of local as global Z.
# Start point global: (0, gap_width/2, handle_height).
# Tangent global: (0, 1, 0).
# Plane needed: XZ plane shifted to y = gap_width/2.

profile = (
    cq.Workplane("XZ")
    .workplane(offset=gap_width/2)
    .moveTo(0, handle_height) # Match the start Z height. X is 0.
    .circle(tube_radius)
)

# Perform the sweep
result = profile.sweep(path_wire)

# Add end caps (optional, but makes it solid/cleaner looking like the image)
# The image shows flat ends. The sweep does this automatically if solid=True (default).