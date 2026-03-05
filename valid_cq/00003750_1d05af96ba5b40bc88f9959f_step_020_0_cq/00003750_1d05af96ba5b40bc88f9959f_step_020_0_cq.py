import cadquery as cq

# --- Parameters ---
# Dimensions estimated from the visual proportions of the image
total_length = 50.0  # Overall length of the part
outer_radius_main = 6.0  # Radius of the main middle section
outer_radius_end = 4.0   # Radius of the smaller end sections
bore_radius = 2.5        # Radius of the central hole

# Lengths of the individual sections
# 1. Left head
# 2. Narrow neck
# 3. Main body
# 4. Right step
left_head_length = 10.0
neck_length = 3.0
neck_radius = 3.5
main_body_length = 27.0
right_step_length = 10.0

# --- Construction ---

# Use the Z-axis for the main axis of revolution for simplicity

# 1. Create the main central body
main_body = cq.Workplane("XY").circle(outer_radius_main).extrude(main_body_length)

# 2. Create the left head
# It's separated from the main body by a neck, but let's build the stack first.
# We will offset the workplane to the top of the main body (which is currently at z=main_body_length)
# But wait, looking at the image, it's easier to think of it as a stack of cylinders.

# Let's restart the construction strategy: build a single profile and revolve it, 
# or stack cylinders. Stacking cylinders is very readable in CadQuery.

# Start from one end (let's say the left side, the "head")
# Section 1: The Head
part = cq.Workplane("XY").circle(outer_radius_main).extrude(left_head_length)

# Section 2: The Neck (narrower)
part = part.faces(">Z").workplane().circle(neck_radius).extrude(neck_length)

# Section 3: The Main Body
part = part.faces(">Z").workplane().circle(outer_radius_main).extrude(main_body_length)

# Section 4: The Right Step (narrower)
part = part.faces(">Z").workplane().circle(outer_radius_end).extrude(right_step_length)

# --- Fillets and Chamfers ---
# Looking at the image, there are fillets/chamfers.
# There is a noticeable chamfer or small fillet on the very front face (right side).
part = part.faces(">Z").edges().chamfer(0.5)

# There might be a slight fillet on the main body edges, but they look fairly sharp 
# except for possibly the transition at the neck. Let's add a small fillet at the neck for realism.
# The neck connects Section 1 and Section 3.
# We need to select the edges belonging to the neck cylinder.
# A robust way is to select edges near the Z-height of the neck.
z_neck_start = left_head_length
z_neck_end = left_head_length + neck_length

# Fillet the transition from Head to Neck
# part = part.edges(f"|Z and >Z[{z_neck_start-0.1}] and <Z[{z_neck_start+0.1}]").fillet(0.5)
# Note: CadQuery selectors can be tricky on complex unions. 
# Simpler approach: no fillets on the neck groove based on the low-res image, it looks like a clean cut.

# --- The Bore (Hole) ---
# The part appears to be hollow or at least has a hole on the visible end.
# Assuming it's a through-hole or a deep blind hole. Let's make it a through-hole.
result = part.faces(">Z").workplane().circle(bore_radius).cutThruAll()

# If it needs to be oriented like the image (roughly isometric view looking down):
# The current default view of the result usually works well, 
# but we can rotate it if strictly necessary to match the axis.
# The image shows the axis roughly along X or Y. Currently ours is along Z.
result = result.rotate((0,0,0), (0,1,0), -90) # Rotate -90 around Y to point along X
