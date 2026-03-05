import cadquery as cq
import math

# Socket head cap screw
# Parameters
head_diameter = 10.0
head_height = 10.0
shaft_diameter = 6.0
shaft_length = 36.0
hex_socket_size = 4.0  # across flats
hex_socket_depth = 5.0
thread_pitch = 1.0
chamfer_size = 0.5

# Build the head (cylinder)
head = (
    cq.Workplane("XY")
    .circle(head_diameter / 2)
    .extrude(head_height)
)

# Add chamfer to top edge of head
head = head.faces(">Z").chamfer(chamfer_size)

# Add chamfer to bottom edge of head
head = head.faces("<Z").chamfer(chamfer_size)

# Cut hex socket into top of head
hex_socket = (
    cq.Workplane("XY")
    .workplane(offset=head_height)
    .polygon(6, hex_socket_size / math.cos(math.radians(30)))
    .extrude(hex_socket_depth, combine=False)
)

head = head.cut(hex_socket)

# Build the shaft
shaft = (
    cq.Workplane("XY")
    .workplane(offset=-shaft_length)
    .circle(shaft_diameter / 2)
    .extrude(shaft_length)
)

# Combine head and shaft
screw_body = head.union(shaft)

# Add thread representation using a helix-like approach
# We'll simulate threads by cutting grooves using torus shapes
# Place thread grooves along the shaft
thread_depth = 0.4
thread_radius = shaft_diameter / 2

# Create thread grooves by subtracting torus rings along the shaft
thread_cutter = cq.Workplane("XY")

# Build individual thread rings and union them
cuts = []
z_pos = -shaft_length + thread_pitch / 2

while z_pos < -chamfer_size:
    # Create a torus-like groove
    # Use revolve to create a ring
    ring = (
        cq.Workplane("XZ")
        .workplane(offset=0)
        .transformed(offset=cq.Vector(0, 0, z_pos))
    )
    
    # Create a small triangular profile and revolve
    r_outer = thread_radius + 0.1
    r_inner = thread_radius - thread_depth
    
    pts = [
        (r_inner, -thread_pitch * 0.4),
        (r_outer, 0),
        (r_inner, thread_pitch * 0.4),
    ]
    
    groove = (
        cq.Workplane("XZ")
        .transformed(offset=cq.Vector(0, 0, z_pos))
        .polyline(pts)
        .close()
        .revolve(360, (0, 0, 0), (0, 0, 1))
    )
    
    cuts.append(groove)
    z_pos += thread_pitch

# Union all cuts together then subtract from screw body
if cuts:
    thread_cuts = cuts[0]
    for c in cuts[1:]:
        thread_cuts = thread_cuts.union(c)
    
    screw_body = screw_body.cut(thread_cuts)

# Add chamfer/taper at tip of shaft
tip_cutter = (
    cq.Workplane("XY")
    .workplane(offset=-shaft_length - 1)
    .circle(shaft_diameter / 2 + 1)
    .workplane(offset=2.5)
    .circle(0.1)
    .loft()
)

screw_body = screw_body.cut(tip_cutter)

result = screw_body