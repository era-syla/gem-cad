import cadquery as cq

# --- Parameters ---

# Stair dimensions
stair_width = 100.0
step_rise = 18.0
step_run = 25.0
num_steps = 10
base_solid_thickness = 20.0  # Thickness of the solid block under the steps if needed, 
                             # but here it looks like a solid block down to the floor.

# Floor/Landing dimensions
floor_thickness = 10.0
floor_extension_front = 150.0 # Length of floor in front of stairs
floor_extension_side = 50.0   # Width of floor on the open side

# Wall dimensions
wall_thickness = 20.0
wall_height_extra = 100.0 # Height of wall above the top step/landing
wall_depth = (num_steps * step_run) + floor_extension_front

# Railing dimensions
post_width = 10.0
post_height = 90.0
handrail_radius = 4.0
baluster_radius = 1.5
baluster_spacing = 15.0 # Center-to-center

# --- Geometry Construction ---

# 1. Create the Stair Block
# We'll create a profile in the YZ plane and extrude it in X.

total_run = num_steps * step_run
total_rise = num_steps * step_rise

stair_profile = [(0, 0)] # Bottom left corner (relative to start of stairs)

# Create the jagged step profile
current_x = 0
current_y = 0
for i in range(num_steps):
    current_y += step_rise
    stair_profile.append((current_x, current_y)) # Vertical riser
    current_x += step_run
    stair_profile.append((current_x, current_y)) # Horizontal tread

# Close the profile
stair_profile.append((total_run, 0)) # Bottom right corner
stair_profile.append((0, 0)) # Back to origin

# Create the solid stair mass
stairs = (
    cq.Workplane("YZ")
    .polyline(stair_profile)
    .close()
    .extrude(stair_width)
)

# Move stairs to correct position relative to global origin
# Let's say origin is at the bottom corner where the wall meets the floor and first step starts.
# Extrude went in +X, profile was Y(up) Z(forward). 
# Wait, default "YZ" plane: X is normal. polyline uses (y, z) coordinates on that plane.
# So (0,0) is origin. (current_x, current_y) in loop corresponds to (Y, Z) in local plane.
# Actually, let's map: 
#   Step Rise is usually Z (vertical).
#   Step Run is usually Y (horizontal depth).
#   Stair Width is X.
# Let's adjust the plane to make it intuitive.
# Let's build on "Right" plane (YZ), where Y is horizontal forward, Z is vertical up.

stair_pts = [(0,0)]
cur_y = 0 # Horizontal run distance
cur_z = 0 # Vertical rise distance
for _ in range(num_steps):
    cur_z += step_rise
    stair_pts.append((cur_y, cur_z))
    cur_y += step_run
    stair_pts.append((cur_y, cur_z))

# Close loop down to the floor
stair_pts.append((cur_y, 0))
stair_pts.append((0, 0))

stairs = (
    cq.Workplane("YZ")
    .polyline(stair_pts)
    .close()
    .extrude(-stair_width) # Extrude in -X direction
)

# 2. Create the Wall
# The wall is on the "left" side (towards positive X relative to the stair width extrusion direction, 
# but since we extruded -X, the wall is at X=0).
# Wall extends behind the stairs and above.

wall_height = total_rise + wall_height_extra
wall_length = total_run + 20 # Slight overhang at top

wall = (
    cq.Workplane("XY")
    .rect(wall_thickness, wall_length, centered=False) # X thickness, Y length
    .extrude(wall_height)
    .translate((-wall_thickness, 0, 0)) # Position against the stairs
)
# Add the cylindrical handrail attached to the wall
wall_rail_height = total_rise + 30 # Rough height relative to top
# It needs to follow the slope.
slope_angle = 35.0 # Approximation
wall_handrail_length = total_run * 1.1
wall_handrail = (
    cq.Workplane("YZ")
    .circle(handrail_radius)
    .extrude(wall_handrail_length)
    .rotate((0,0,0), (1,0,0), -slope_angle) # Tilt it
    .translate((-wall_thickness/2, total_run/2, total_rise/2 + 40)) # Position roughly
    # This is tricky to align perfectly parametrically without trig, doing a simpler approximation:
    # Let's define start and end points
)

# Alternative Wall Handrail: Loft or Sweep
p1 = (-wall_thickness/2, 0, step_rise*2 + 40)
p2 = (-wall_thickness/2, total_run, total_rise + 40)
wall_handrail = (
    cq.Workplane("YZ")
    .transformed(offset=p1, rotate=(0,0,0)) # Start point
    .circle(handrail_radius)
    .workplane(offset=0) # Reset workplane logic
    .transformed(offset=p2, rotate=(0,0,0)) # This doesn't sweep directly easily like this.
)
# Simpler: Create a cylinder and rotate/move it.
import math
angle = math.degrees(math.atan(step_rise/step_run))
rail_len = math.sqrt(total_rise**2 + total_run**2)
wall_handrail = (
    cq.Workplane("YZ")
    .circle(handrail_radius)
    .extrude(rail_len + 20)
    .rotate((0,0,0), (1,0,0), -angle)
    .translate((-wall_thickness/2, -10, 90)) # Adjust starting position
)


# 3. Create the Floor
# Extends under the stairs and out to the side/front.
floor = (
    cq.Workplane("XY")
    .rect(stair_width + floor_extension_side + wall_thickness, 
          total_run + floor_extension_front, centered=False)
    .extrude(-floor_thickness)
    .translate((-wall_thickness, 0, 0))
)

# 4. Create the Railing System (Open Side)
# Located at X = -stair_width
rail_x = -stair_width + post_width/2

# Newel Post (Bottom) - actually visual shows post at top mainly
# Let's put a post at the top landing
top_post_pos = (rail_x, total_run - step_run/2, total_rise)
top_post = (
    cq.Workplane("XY")
    .rect(post_width, post_width)
    .extrude(post_height)
    .translate((top_post_pos[0], top_post_pos[1], top_post_pos[2]))
)

# Add a sphere on top of the post
post_cap = (
    cq.Workplane("XY")
    .sphere(post_width * 0.8)
    .translate((top_post_pos[0], top_post_pos[1], top_post_pos[2] + post_height))
)

# Bottom Post (Bottom step)
bot_post_pos = (rail_x, step_run/2, step_rise)
# In image, rail just goes into wall or starts at first step. 
# Let's put a small start post.
# Actually, looks like railing starts from a point on the wall/slope and goes to the top post.
# We will make a sloping handrail and vertical balusters.

# Slope Rail
rail_start_pt = (rail_x, 0, 90) # Relative to stair start
rail_end_pt = (rail_x, total_run - step_run/2, total_rise + post_height - 10)

# Vector math for length and angle
dy = rail_end_pt[1] - rail_start_pt[1]
dz = rail_end_pt[2] - rail_start_pt[2]
rail_length = math.sqrt(dy**2 + dz**2)
rail_angle = math.degrees(math.atan2(dz, dy))

sloped_rail = (
    cq.Workplane("YZ")
    .workplane(centerOption="ProjectedOrigin")
    .center(rail_start_pt[1], rail_start_pt[2])
    .rect(post_width, post_width) # Rectangular handrail
    .extrude(rail_length)
    .rotate((rail_start_pt[1], rail_start_pt[2], 0), (1,0,0), -rail_angle) # Rotate around start point axis
    .translate((rail_x, 0, 0))
)

# Balusters
balusters = cq.Assembly()
# Distribute along the Y axis
current_baluster_y = step_run
while current_baluster_y < (total_run - step_run):
    # Calculate height at this Y based on slope
    ratio = current_baluster_y / total_run
    # Interpolate height roughly
    # Base Z is the step height at this Y
    step_idx = int(current_baluster_y / step_run)
    base_z = (step_idx + 1) * step_rise
    
    # Rail Z calculation (linear equation line)
    # z = m*y + c
    slope = dz/dy
    rail_z_at_y = slope * (current_baluster_y - rail_start_pt[1]) + rail_start_pt[2]
    
    baluster_height = rail_z_at_y - base_z
    
    if baluster_height > 0:
        bal = (
            cq.Workplane("XY")
            .circle(baluster_radius)
            .extrude(baluster_height)
            .translate((rail_x, current_baluster_y, base_z))
        )
        balusters.add(bal)
        
    current_baluster_y += baluster_spacing

# Combine everything
result = (
    stairs
    .union(wall)
    .union(wall_handrail)
    .union(floor)
    .union(top_post)
    .union(post_cap)
    .union(sloped_rail)
)

# Union the balusters (iterating the assembly components logic for a single solid result)
# Since Assembly isn't a solid, we union the underlying solids.
for b in balusters.shapes:
    result = result.union(b)

# Final cleanup or orientation if needed
# The current model is Y-forward, Z-up. This is standard for mechanical CAD.