import cadquery as cq

# --- Parameters ---
# Dimensions estimated from the visual proportions of the U-bolt
rod_diameter = 10.0      # Thickness of the rod
bend_radius = 25.0       # Internal radius of the curve
leg_length = 80.0        # Total straight length of the legs
thread_length = 40.0     # Length of the threaded portion (simulated)
thread_pitch = 1.5       # Pitch for the cosmetic threads
thread_depth = 0.5       # Depth of cut for threads

# Derived parameters
center_distance = bend_radius * 2 + rod_diameter
# Calculating the path points
# We will create a path: straight leg -> semi-circle arc -> straight leg

# --- Geometry Construction ---

# 1. Create the Path
# The U-bolt stands vertically. Let's orient it so the legs point down (-Z)
# and the bend is at the top.
# Left leg start point
p1 = (- (bend_radius + rod_diameter/2), 0, -leg_length)
# Left leg end of straight section (start of arc)
p2 = (- (bend_radius + rod_diameter/2), 0, 0)
# Top of arc
p3 = (0, 0, bend_radius + rod_diameter/2)
# Right leg start of straight section (end of arc)
p4 = ((bend_radius + rod_diameter/2), 0, 0)
# Right leg end point
p5 = ((bend_radius + rod_diameter/2), 0, -leg_length)

# Define the path
path = (
    cq.Workplane("XZ")
    .moveTo(p1[0], p1[2])
    .lineTo(p2[0], p2[2])
    .threePointArc(p3, (p4[0], p4[2]))
    .lineTo(p5[0], p5[2])
)

# 2. Sweep the main rod profile
# Create the circular cross-section and sweep it along the path
u_bolt_body = (
    cq.Workplane("XY")
    .workplane(offset=-leg_length) # Move to the start of the leg
    .center(p1[0], p1[1])          # Center on the path start
    .circle(rod_diameter / 2.0)
    .sweep(path)
)

# 3. Create Simulated Threads
# True helical threads are computationally expensive and often unnecessary for visualization.
# We will create a series of annular grooves to simulate the look of threads.

def create_thread_cutter(loc_coords):
    """Creates a cutting tool for the threads at a specific X,Y location."""
    x, y = loc_coords
    
    # Create a profile for the thread groove (triangular cut)
    # We create a single ring cutter
    thread_profile = (
        cq.Workplane("XZ")
        .workplane(offset=y)
        .moveTo(x + rod_diameter/2, -leg_length) # Start at bottom of leg, outer surface
        .lineTo(x + rod_diameter/2 - thread_depth, -leg_length + thread_pitch/2)
        .lineTo(x + rod_diameter/2, -leg_length + thread_pitch)
        .close()
        .revolve(360, (x, 0, 0), (x, 0, 1)) # Revolve around the leg axis
    )
    
    # Create a stack of these rings
    num_threads = int(thread_length / thread_pitch)
    
    # Pattern the single thread ring upwards
    # Note: Using a loop here or a linear pattern on the solid
    threads = (
        cq.Workplane("XY")
        .add(thread_profile.val())
        .toPending()
    )
    
    # Array/Pattern the cut solid
    # We do this by creating a linear array of points and placing the cutter
    # Since we already have a solid, we can just use newWorkplane and pattern
    # However, creating a union of solids first is often robust in CQ
    
    cutters = []
    for i in range(num_threads):
        z_offset = i * thread_pitch
        cutters.append(thread_profile.translate((0, 0, z_offset)))
        
    # Combine all cutters into one object
    combined_cutter = cutters[0]
    for c in cutters[1:]:
        combined_cutter = combined_cutter.union(c)
        
    return combined_cutter

# Generate cutters for left and right legs
left_leg_x = p1[0]
right_leg_x = p5[0]

# Generating complex unions can be slow, simplified approach:
# We perform the cut operation directly.

# Create a simplified cylinder to subtract for threads (faster than revolving triangles)
# Or stick to grooves for the visual fidelity requested. Let's do the grooves.

# Optimization: Create one cutter stack and translate it
# Build one thread ring
base_thread_ring = (
    cq.Workplane("XZ")
    .moveTo(rod_diameter/2, 0)
    .lineTo(rod_diameter/2 - thread_depth, thread_pitch/2)
    .lineTo(rod_diameter/2, thread_pitch)
    .close()
    .revolve(360, (0,0,0), (0,0,1))
)

# Stack them
thread_stack = base_thread_ring
for i in range(1, int(thread_length / thread_pitch)):
    thread_stack = thread_stack.union(base_thread_ring.translate((0, 0, i * thread_pitch)))

# Position stacks on the legs
left_threads = thread_stack.translate((left_leg_x, 0, -leg_length))
right_threads = thread_stack.translate((right_leg_x, 0, -leg_length))

# Apply the cuts
result = u_bolt_body.cut(left_threads).cut(right_threads)