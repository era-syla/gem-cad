import cadquery as cq
import math

# Socket head cap screw (M6 x 25 approximate dimensions)
# Parameters
head_diameter = 10.0
head_height = 6.0
shaft_diameter = 6.0
shaft_length = 25.0
hex_socket_across_flats = 5.0
hex_socket_depth = 3.0
thread_pitch = 1.0
chamfer_size = 0.3

# Build the screw head
head = (
    cq.Workplane("XY")
    .circle(head_diameter / 2)
    .extrude(head_height)
)

# Chamfer top edge of head
head = head.faces(">Z").chamfer(chamfer_size)

# Chamfer bottom edge of head
head = head.faces("<Z").chamfer(chamfer_size)

# Cut hex socket into the top of the head
hex_diameter = hex_socket_across_flats / math.cos(math.radians(30))
head = (
    head
    .faces(">Z")
    .workplane()
    .polygon(6, hex_diameter)
    .cutBlind(hex_socket_depth)
)

# Build the shaft (smooth shank + threaded appearance)
shaft = (
    cq.Workplane("XY")
    .workplane(offset=-shaft_length)
    .circle(shaft_diameter / 2)
    .extrude(shaft_length)
)

# Chamfer the bottom tip of the shaft
shaft = shaft.faces("<Z").chamfer(chamfer_size * 2)

# Add thread profile approximation using a series of grooves
# We simulate threads by creating a cylinder with helical groove appearance
# Since helix isn't available, we approximate with stacked torus cuts

thread_start_z = -shaft_length
num_threads = int(shaft_length / thread_pitch)
thread_depth = 0.4
thread_radius = shaft_diameter / 2

# Create threaded shaft by cutting grooves to simulate threads
threaded_shaft = shaft
for i in range(num_threads):
    z_pos = thread_start_z + i * thread_pitch + thread_pitch / 2
    # Create a torus-like groove at each thread position
    groove = (
        cq.Workplane("XY")
        .workplane(offset=z_pos)
        .circle(thread_radius + 0.01)
        .circle(thread_radius - thread_depth)
        .extrude(thread_pitch * 0.6)
    )
    threaded_shaft = threaded_shaft.cut(groove)

# Combine head and shaft
result = head.union(threaded_shaft)