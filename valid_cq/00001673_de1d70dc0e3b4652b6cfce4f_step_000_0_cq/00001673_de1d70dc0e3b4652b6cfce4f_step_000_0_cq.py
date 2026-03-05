import cadquery as cq

# --- Parametric Dimensions ---
# Main Frame Dimensions
frame_width_rear = 120.0  # Width of the rectangular rear section
frame_length_rear = 150.0 # Length of the straight rear section
frame_width_front = 180.0 # Total width of the front crossbar
frame_length_front = 80.0 # Length of the converging section
tube_size = 10.0          # Square tube cross-section size
tube_wall = 1.5           # Wall thickness (if we were hollowing, but solid is usually simpler for visual)

# Front converging angle calculations could be done, but setting coordinates is more direct
# We will model the path and sweep a profile along it.

# Hitch/Coupler Dimensions
hitch_post_height = 40.0
hitch_bracket_size = 15.0
hitch_hole_dia = 6.0
tongue_length = 25.0

# Axle/Steering mount dimensions (cylinders at ends of front bar)
axle_mount_height = 25.0
axle_mount_dia = 12.0
axle_mount_hole = 8.0

# --- Geometry Construction ---

# 1. Main Frame Path Generation
# We'll define the centerline points of the frame
# Origin (0,0) will be the center of the rear rectangle

p_rear_left = (-frame_width_rear/2, -frame_length_rear)
p_rear_right = (frame_width_rear/2, -frame_length_rear)
p_mid_left = (-frame_width_rear/2, 0)
p_mid_right = (frame_width_rear/2, 0)

# Front converging points
# The front bar is wider, located forward in Y
p_front_left = (-frame_width_front/2, frame_length_front)
p_front_right = (frame_width_front/2, frame_length_front)
p_front_center = (0, frame_length_front) # Center of the front bar

# Helper function to create a square tube sweep between points
def make_tube(p1, p2, size):
    path = cq.Workplane("XY").moveTo(p1[0], p1[1]).lineTo(p2[0], p2[1])
    return (cq.Workplane("YZ")
            .rect(size, size)
            .sweep(path)
           )

# Create the frame segments
# Rear Rectangle sides
rear_bar = make_tube(p_rear_left, p_rear_right, tube_size)
left_side = make_tube(p_rear_left, p_mid_left, tube_size)
right_side = make_tube(p_rear_right, p_mid_right, tube_size)

# Converging front section
left_converge = make_tube(p_mid_left, p_front_center, tube_size)
right_converge = make_tube(p_mid_right, p_front_center, tube_size)

# Front Crossbar
front_bar = make_tube(p_front_left, p_front_right, tube_size)

# Assemble basic frame
frame = (rear_bar
         .union(left_side)
         .union(right_side)
         .union(left_converge)
         .union(right_converge)
         .union(front_bar)
        )

# 2. Central Structural Spine (from rear mid to front mid)
# Looking at the image, there's a spine running from the back of the converging section
# towards the front, but it looks like it supports the hitch.
# Actually, the image shows a Y-shape frame. The center spine seems to start 
# near the convergence point and go backwards?
# Let's look closer. It looks like a kart chassis.
# There is a rear rectangle, then tubes converge to the center, then a front beam.
# Re-evaluating the topology based on the "Y" shape often seen in karts:
# Rectangular back section.
# Then tubes converge to a SINGLE point at the front beam center?
# The image actually shows the side rails angling inward to meet the front beam, 
# but they meet the front beam at an offset, not the center.
# Wait, looking at the image:
# - Back is a U-shape (rectangle without front side).
# - Then angled tubes go from the open ends of the U to the CENTER of the front bar.
# - The front bar is a wide straight bar.
# - There is a center tube running from the convergence point backwards slightly to hold the hitch? 
# No, looking at the crop: 
# The angled tubes meet at the center of the front bar.
# There is a central tube running from that intersection BACKWARDS to support the steering column/hitch.
# Let's adjust the topology logic.

# Adjusted Topology:
# 1. Rear U-shape (Back, Left, Right)
# 2. Angled tubes from Left/Right ends to Front-Center.
# 3. Front Crossbar (Left-Front to Right-Front) crossing through Front-Center.
# 4. Steering/Hitch column structure in the middle.

# Let's refine the "converging" tubes to meet exactly at (0, frame_length_front)
# And the front bar passes through that point.
# The previous code for `left_converge` and `right_converge` does exactly this.

# 3. Steering Knuckle / Kingpin Tubes (Cylinders at ends of front bar)
# These are vertical cylinders at the tips of the front bar.
def make_kingpin(x_pos, y_pos):
    return (cq.Workplane("XY")
            .center(x_pos, y_pos)
            .circle(axle_mount_dia/2)
            .extrude(axle_mount_height/2, both=True)
            .faces(">Z").workplane()
            .hole(axle_mount_hole)
           )

left_kingpin = make_kingpin(p_front_left[0], p_front_left[1])
right_kingpin = make_kingpin(p_front_right[0], p_front_right[1])

# 4. Center Assembly (Hitch/Steering Column)
# It's located on the centerline, somewhat back from the front convergence point.
# There is a vertical post and a horizontal bracket.

# Position for the column
column_y = frame_length_front * 0.3 # Between 0 and front
column_x = 0

# Vertical Post
post = (cq.Workplane("XY")
        .center(column_x, column_y)
        .rect(tube_size, tube_size)
        .extrude(hitch_post_height)
       )

# Support tube for the post (connecting post to the converging tubes)
# It looks like a small piece of tube running along Y axis connecting the post to the front junction
support_tube = make_tube((0, column_y), p_front_center, tube_size)

# Bracket on top of the post
# It looks like a C-bracket or a plate with a hole
bracket_z = hitch_post_height - tube_size/2
bracket = (cq.Workplane("XY")
           .workplane(offset=bracket_z)
           .center(column_x, column_y)
           .box(hitch_bracket_size, tongue_length + tube_size, tube_size)
           .faces(">Z").workplane() # Work on top
           .center(0, -tongue_length/2) # Move towards the "tongue"
           .hole(hitch_hole_dia)
          )

# The weird L-shaped piece sticking out of the bracket in the image
# It looks like a steering linkage mount pointing sideways/backwards.
# Let's approximate it as a plate sticking out to the left (-X)
linkage_arm = (cq.Workplane("XY")
               .workplane(offset=bracket_z)
               .center(column_x - hitch_bracket_size/2, column_y)
               .box(25, 10, 5, centered=(False, True, True)) # Extrude in -X direction
               .rotate((0,0,0), (0,0,1), 160) # Angle it back slightly
               .faces(">Z").workplane()
               .center(20, 0)
               .hole(5)
              )

# 5. Final Boolean Operations
result = (frame
          .union(left_kingpin)
          .union(right_kingpin)
          .union(post)
          .union(support_tube)
          .union(bracket)
          .union(linkage_arm)
         )

# Add fillets to smooth transitions (optional but makes it look like welded tubing)
result = result.edges("|Z").fillet(1.0)
