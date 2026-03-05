import cadquery as cq
import math

# Socket head cap screw
# Parameters
head_diameter = 10.0
head_height = 10.0
shaft_diameter = 6.0
shaft_length = 35.0
hex_key_size = 4.0  # across flats
thread_pitch = 1.0
chamfer_size = 0.5

# Build the screw head (cylindrical)
head = (
    cq.Workplane("XY")
    .cylinder(head_height, head_diameter / 2)
)

# Translate head up so it sits on top of shaft
head = head.translate((0, 0, shaft_length + head_height / 2))

# Build the shaft (cylinder)
shaft = (
    cq.Workplane("XY")
    .cylinder(shaft_length, shaft_diameter / 2)
    .translate((0, 0, shaft_length / 2))
)

# Union head and shaft
screw = head.union(shaft)

# Add thread simulation using a helix-like approach
# We'll simulate threads by cutting a helical groove
# Using a simple approach: stack of slightly overlapping torus cuts
# Actually, let's use a profile revolution approach for threads

# Create thread profile cuts along the shaft
# Use a series of torus-like grooves to simulate threads
thread_result = cq.Workplane("XY")

# Build the base screw body first
base = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .circle(shaft_diameter / 2)
    .extrude(shaft_length)
)

# Add head on top
head_solid = (
    cq.Workplane("XY")
    .workplane(offset=shaft_length)
    .circle(head_diameter / 2)
    .extrude(head_height)
)

screw_body = base.union(head_solid)

# Chamfer bottom of shaft
screw_body = screw_body.faces("<Z").chamfer(chamfer_size)

# Chamfer top edge of head
screw_body = screw_body.faces(">Z").chamfer(chamfer_size)

# Add hex socket in the head
socket_depth = 5.0
hex_diameter = hex_key_size / math.cos(math.radians(30))  # circumscribed circle

screw_body = (
    screw_body
    .faces(">Z")
    .workplane()
    .polygon(6, hex_diameter)
    .cutBlind(-socket_depth)
)

# Simulate threads by cutting helical grooves
# We approximate with a series of angled cuts
thread_start = 0.5
thread_end = shaft_length - 0.5
n_threads = int((thread_end - thread_start) / thread_pitch)

thread_depth = 0.4
thread_radius = shaft_diameter / 2

# Create thread grooves as torus sections
# We'll use a wire sweep approach
# Build a helical thread using swept profile

# Create the helical path points
def make_helix_wire(pitch, height, radius, center=(0,0,0)):
    """Create a helix as a series of line segments approximating a helix."""
    import cadquery as cq
    n_turns = height / pitch
    n_points = int(n_turns * 24) + 1
    points = []
    for i in range(n_points):
        t = i / (n_points - 1)
        angle = t * n_turns * 2 * math.pi
        z = center[2] + t * height
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        points.append((x, y, z))
    return points

# Instead of complex helix, use stacked torus cuts for thread simulation
thread_body = screw_body

for i in range(n_threads + 1):
    z_pos = thread_start + i * thread_pitch
    if z_pos > thread_end:
        break
    # Cut a small groove at this z position using a torus approximation
    # Use a thin disk cut at angle
    groove = (
        cq.Workplane("XZ")
        .workplane(offset=0)
        .transformed(offset=cq.Vector(0, 0, z_pos))
        .circle(thread_radius + thread_depth)
        .circle(thread_radius - 0.1)
        .extrude(thread_pitch * 0.5)
    )

# Simpler thread approach: use revolve of a sawtooth profile
# Create a 2D thread profile in the XZ plane and revolve
thread_profile_pts = []
z = thread_start
r_outer = shaft_diameter / 2
r_inner = r_outer - thread_depth

thread_profile_pts.append((r_inner - 0.01, thread_start - 0.1))
for i in range(n_threads + 2):
    z_base = thread_start + i * thread_pitch
    if z_base > thread_end + thread_pitch:
        break
    thread_profile_pts.append((r_outer, z_base))
    thread_profile_pts.append((r_inner, z_base + thread_pitch * 0.5))

thread_profile_pts.append((r_inner - 0.01, thread_end + 0.1))

# Create thread solid via revolve
thread_solid = (
    cq.Workplane("XZ")
    .polyline(thread_profile_pts)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)

# Subtract thread solid from screw to create grooves
# Actually intersect with shaft region then subtract
result = screw_body.cut(thread_solid)