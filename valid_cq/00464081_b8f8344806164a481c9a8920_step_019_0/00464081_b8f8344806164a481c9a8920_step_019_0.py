import cadquery as cq
import math

# ==========================================
# Parameters (Metric Hex Bolt M12 x 80)
# ==========================================
bolt_dia = 12.0               # Shaft diameter
bolt_length = 80.0            # Length of shaft
head_height = 7.5             # Thickness of the hex head
head_flat_to_flat = 18.0      # Wrench size
thread_length = 25.0          # Length of the threaded section
thread_pitch = 1.75           # Pitch of the threads
chamfer_angle = 30.0          # Angle for head top chamfer

# Derived Dimensions
head_radius = head_flat_to_flat / (2 * math.cos(math.radians(30)))
shaft_radius = bolt_dia / 2.0
thread_depth = 0.6134 * thread_pitch # Approximate metric thread depth

# ==========================================
# Geometry Construction
# ==========================================

# 1. Create the Hex Head
# We create a hexagon on the XY plane and extrude it.
head = (
    cq.Workplane("XY")
    .polygon(6, head_radius * 2) # polygon takes circumdiameter
    .extrude(head_height)
)

# 2. Chamfer the Top of the Head
# Standard bolts have a conical chamfer on the top face to remove sharp corners.
# We create a profile to revolve-cut the corners.
# The cut starts at the flat-to-flat diameter and cuts outwards/downwards.
c_cut_p1 = (head_flat_to_flat / 2.0, head_height)
c_cut_p2 = (head_radius * 1.1, head_height) # Point outside
# Calculate P3 based on angle
# tan(angle) = dy / dx -> dy = dx * tan(angle)
dx = c_cut_p2[0] - c_cut_p1[0]
dy = dx * math.tan(math.radians(chamfer_angle))
c_cut_p3 = (c_cut_p2[0], head_height - dy)

chamfer_cutter = (
    cq.Workplane("XZ")
    .polyline([c_cut_p1, c_cut_p2, c_cut_p3, c_cut_p1])
    .close()
    .revolve()
)

head = head.cut(chamfer_cutter)

# 3. Create the Shaft
# Extrude cylinder from the bottom of the head
shaft = (
    head.faces("<Z")
    .workplane()
    .circle(shaft_radius)
    .extrude(bolt_length)
)

# 4. Chamfer the Tip of the Shaft
# Select the edge at the very bottom (furthest Z)
bolt_body = shaft.faces("<Z").edges().chamfer(thread_pitch * 0.75)

# 5. Create Threads (Visual Representation)
# We use annular grooves to simulate threads efficiently and robustly.
# This involves revolving a "comb" profile to cut the grooves.

# Define the Z-range for threads relative to the origin
# Head is 0 to head_height. Shaft goes down to -(bolt_length) if we extruded down? 
# In step 3 we extruded from <Z face. The head is 0..7.5. The face <Z is at 0.
# So the shaft goes from 0 to +80 in the workplane's local Z, which corresponds to global 0 to -80?
# CadQuery extrude works along normal. Face <Z normal is (0,0,-1). 
# So shaft extends from Z=0 to Z=-80.

# Thread section is at the bottom: from Z = -80 + thread_length to -80.
z_bottom = -bolt_length
z_top_thread = -bolt_length + thread_length

# Generate profile points for the cutter
# We start at the surface of the shaft and zigzag inwards
cutter_pts = []
cutter_pts.append((shaft_radius, z_top_thread)) # Start top of thread section on surface

num_threads = int(thread_length / thread_pitch)

for i in range(num_threads):
    # Current Z level moving down
    z_curr = z_top_thread - (i * thread_pitch)
    
    # Create a V-groove
    # Top of V
    p_top = (shaft_radius, z_curr - (thread_pitch * 0.1))
    # Bottom of V (deepest cut)
    p_deep = (shaft_radius - thread_depth, z_curr - (thread_pitch * 0.5))
    # Bottom of V (return to surface)
    p_bot = (shaft_radius, z_curr - (thread_pitch * 0.9))
    
    cutter_pts.append(p_top)
    cutter_pts.append(p_deep)
    cutter_pts.append(p_bot)

cutter_pts.append((shaft_radius, z_bottom)) # End at bottom surface

# Close the loop to make a valid face for revolution
# We need to go out to a larger radius to ensure we define a solid "tool" to remove
safe_radius = shaft_radius * 1.5
cutter_pts.append((safe_radius, z_bottom))
cutter_pts.append((safe_radius, z_top_thread))
cutter_pts.append((shaft_radius, z_top_thread)) # Close

# Create the cutting tool
thread_cutter = (
    cq.Workplane("XZ")
    .polyline(cutter_pts)
    .close()
    .revolve()
)

# Apply the cut
result = bolt_body.cut(thread_cutter)

# Export or Render
if 'show_object' in globals():
    show_object(result)