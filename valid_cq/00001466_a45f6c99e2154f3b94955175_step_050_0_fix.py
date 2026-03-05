import cadquery as cq
import math

# Parameters
body_r = 8.0        # threaded body radius
body_h = 30.0       # threaded body height
thread_pitch = 2.5  # thread pitch
thread_depth = 1.2  # thread depth

top_collar_r = 7.0  # collar under barb
top_collar_h = 3.0

barb_r = 5.0        # barb fitting radius
barb_h = 8.0
barb_inner_r = 2.5  # through hole radius

base_w = 18.0       # base block width
base_d = 14.0       # base block depth
base_h = 8.0        # base block height

side_port_r = 2.5   # side port radius

# --- Build the threaded body with approximated threads (grooves) ---
# Main cylinder
main_body = (
    cq.Workplane("XY")
    .cylinder(body_h, body_r)
)

# Cut thread grooves as a series of rings
thread_body = main_body
num_threads = int(body_h / thread_pitch)
for i in range(num_threads):
    z_pos = -body_h/2 + i * thread_pitch + thread_pitch/2
    thread_body = (
        thread_body
        .workplane(offset=z_pos)
        .circle(body_r + thread_depth)
        .circle(body_r - thread_depth)
        .extrude(thread_pitch * 0.4, combine=False)
    )

# Rebuild: cylinder with thread grooves cut in
base_cyl = cq.Workplane("XY").cylinder(body_h, body_r)

# Add thread rings on outside using shell approach
# Instead, let's do it properly with cuts
threaded_body = cq.Workplane("XY").cylinder(body_h, body_r + thread_depth)

# Cut thread grooves
for i in range(num_threads + 1):
    z_center = -body_h/2 + i * thread_pitch
    groove_h = thread_pitch * 0.5
    threaded_body = (
        threaded_body
        .workplane(offset=z_center)
        .circle(body_r + thread_depth + 0.1)
        .cutBlind(-groove_h)
    )

# Add top collar
top_z = body_h / 2
assembly = (
    threaded_body
    .workplane(offset=top_z)
    .circle(top_collar_r)
    .extrude(top_collar_h)
)

# Add barb/connector on top
assembly = (
    assembly
    .workplane(offset=top_z + top_collar_h)
    .circle(barb_r)
    .extrude(barb_h)
)

# Add through hole down the center
total_h = body_h + top_collar_h + barb_h
assembly = (
    assembly
    .workplane(offset=top_z + top_collar_h + barb_h)
    .circle(barb_inner_r)
    .cutBlind(-total_h * 1.5)
)

# Add base block at bottom
base_z = -body_h / 2
base_block = (
    cq.Workplane("XY")
    .workplane(offset=base_z - base_h)
    .box(base_w, base_d, base_h, centered=(True, True, False))
)

assembly = assembly.union(base_block)

# Add side port hole in base block
assembly = (
    assembly
    .workplane(offset=base_z - base_h/2)
    .transformed(rotate=(0, 90, 0))
    .circle(side_port_r)
    .cutBlind(base_w)
)

# Add chamfer to top barb edge
assembly = (
    assembly
    .faces(">Z")
    .edges()
    .chamfer(0.5)
)

result = assembly