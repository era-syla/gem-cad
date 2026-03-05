import cadquery as cq
import math

# Parameters
outer_radius = 30
inner_radius = 22
total_length = 55
flange_length = 10
threaded_length = 45
thread_pitch = 2.0
thread_depth = 1.2

# Create the main hollow cylinder (body)
body = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(total_length)
)

# Create flange ring at one end (larger outer diameter)
flange_outer = outer_radius + 4
flange = (
    cq.Workplane("XY")
    .workplane(offset=threaded_length)
    .circle(flange_outer)
    .circle(inner_radius)
    .extrude(flange_length)
)

# Combine body and flange
result = body.union(flange)

# Add threads to the threaded section using helical cuts
# Simulate threads by adding a series of grooves
num_threads = int(threaded_length / thread_pitch)

# Build thread profile as a series of toroidal cuts
thread_shape = None
for i in range(num_threads):
    z_pos = i * thread_pitch + thread_pitch / 2
    if z_pos > threaded_length:
        break
    groove = (
        cq.Workplane("XZ")
        .workplane(offset=0)
        .center(0, z_pos)
        .circle(thread_depth * 0.8)
        .revolve(360, (-(outer_radius + 5), 0), (-(outer_radius + 5), 1))
    )
    if thread_shape is None:
        thread_shape = groove
    else:
        thread_shape = thread_shape.union(groove)

# Alternative approach: create thread grooves using torus-like rings
# Use a cleaner method with swept profiles

# Reset and rebuild with proper threads
# Main body
main_body = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(threaded_length)
)

# Flange at the right end
flange_part = (
    cq.Workplane("XY")
    .workplane(offset=threaded_length)
    .circle(flange_outer)
    .circle(inner_radius)
    .extrude(flange_length)
)

result = main_body.union(flange_part)

# Add thread grooves - use thin rings cut into the outer surface
for i in range(int(threaded_length / thread_pitch)):
    z_center = i * thread_pitch + thread_pitch / 2
    if z_center >= threaded_length:
        break
    
    half_w = thread_pitch * 0.35
    
    groove_cut = (
        cq.Workplane("XY")
        .workplane(offset=z_center - half_w)
        .circle(outer_radius + 1)
        .circle(outer_radius - thread_depth)
        .extrude(half_w * 2)
    )
    result = result.cut(groove_cut)

# Small chamfer on the threaded end
result = (
    result
    .faces(">Z")
    .edges()
    .chamfer(1.0)
)