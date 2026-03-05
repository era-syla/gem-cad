import cadquery as cq

# --- Parametric Dimensions ---
# Hex body parameters
hex_flat_to_flat = 10.0   # Width across flats
hex_height = 30.0         # Length of the hexagonal part

# Threaded section parameters
thread_diameter = 5.0     # M5 usually goes with ~8-10mm hex
thread_length = 8.0       # Length of the threaded stud
thread_pitch = 0.8        # Standard coarse pitch for M5

# Chamfer parameters
chamfer_size = 0.5        # Chamfer on hex edges

# --- Model Construction ---

# 1. Create the Hexagonal Body
# We create a hexagon on the XY plane and extrude it
hex_body = (
    cq.Workplane("XY")
    .polygon(6, hex_flat_to_flat / (3**0.5 / 2) * 0.5 * 2) # circumradius calculation
    .extrude(hex_height)
)

# Apply chamfers to the top and bottom edges of the hex body
hex_body = hex_body.edges("|Z").chamfer(0.2) # Optional: slight vertical edge break
hex_body = hex_body.faces(">Z or <Z").edges().chamfer(chamfer_size)

# 2. Create the Threaded Stud (Simplified)
# Creating a simple cylinder to represent the threaded stud
# CadQuery doesn't render helical threads easily by default for performance,
# but we can simulate the look with a series of disks or just a cylinder.
# Here, we will model the major diameter and add rings to simulate threads visually.

stud_center = hex_body.faces("<Z").workplane().center(0, 0)
stud_core = stud_center.circle(thread_diameter / 2).extrude(thread_length)

# 3. Simulate Threads (Visual representation)
# We create a series of small toruses or cut rings.
# A simpler, more robust visual approximation is a revolved profile.
# For this script, we'll keep it simple: a cylinder with grooves.

# Creating the grooves
num_threads = int(thread_length / thread_pitch)
groove_depth = 0.4 # Approximate depth for visual
groove_width = thread_pitch / 2.0

# Union the stud to the body first
result = hex_body.union(stud_core)

# Cut grooves to simulate threads
for i in range(num_threads):
    # Skip the very beginning and end to make it look clean
    if i < 1 or i > num_threads - 2:
        continue
        
    z_pos = - (i * thread_pitch)
    
    # We cut rings into the stud
    cutter = (
        cq.Workplane("XY")
        .workplane(offset=z_pos)
        .circle(thread_diameter / 2 + 0.1) # Outer boundary of cut
        .circle(thread_diameter / 2 - groove_depth) # Inner boundary of cut
        .extrude(groove_width)
    )
    # Since the stud was extruded in negative Z relative to the workplane if using <Z face,
    # we need to ensure coordinates match.
    # The stud_core was built on the <Z face of the hex (which is at z=0). 
    # The extrude(thread_length) goes in positive normal direction (away from body? No, extrude is positive Z usually).
    # Let's re-verify direction.
    
    # Let's rebuild the stud explicitly downwards to be sure.
    pass

# --- Refined Approach for Robustness ---

# 1. Base Hex
hex_r = hex_flat_to_flat / (3**0.5) # circumradius
base = (
    cq.Workplane("XY")
    .polygon(6, hex_r * 2)
    .extrude(hex_height)
)

# Chamfer the top face edges
base = base.faces(">Z").edges().chamfer(chamfer_size)
# Chamfer the bottom face edges
base = base.faces("<Z").edges().chamfer(chamfer_size)

# 2. The Stud Cylinder
# We extrude downwards from the bottom face
stud = (
    base.faces("<Z").workplane()
    .circle(thread_diameter / 2)
    .extrude(thread_length)
)

# 3. Visual Threads
# We will cut helical-like grooves by subtracting torus-like shapes
# Position starts at the bottom of the hex (Z=0 if hex is 0..30, but creating on face <Z creates local coords)
# Let's work in global coords to be safe. Hex is 0 to 30. Bottom is 0. Stud goes 0 to -8.

def make_thread_groove(i):
    # Position Z relative to the bottom of the hex
    z_offset = -1.0 * (i * thread_pitch + thread_pitch)
    
    # Don't cut past the end
    if z_offset < -(thread_length - thread_pitch):
        return None
        
    groove = (
        cq.Workplane("XY")
        .workplane(offset=z_offset)
        .circle(thread_diameter / 2 + 1) # Outer
        .circle(thread_diameter / 2 - 0.3) # Inner (minor dia approx)
        .extrude(thread_pitch / 2)
    )
    return groove

# Combine
result = stud

# Apply thread cuts
for i in range(int(thread_length / thread_pitch)):
    cut_obj = make_thread_groove(i)
    if cut_obj:
        result = result.cut(cut_obj)

# Add a small chamfer to the tip of the stud
# The tip is the face with the lowest Z value
result = result.faces("<Z").edges().chamfer(0.3)

# Final Result
# 'result' variable is ready