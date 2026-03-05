import cadquery as cq
import math

# Parameters
shaft_diameter = 3.0
shaft_length = 18.0
head_diameter = 5.5
head_height = 2.2
thread_pitch = 0.5
thread_depth = 0.3

# Build the screw shaft (smooth cylinder)
shaft = (
    cq.Workplane("XY")
    .cylinder(shaft_length, shaft_diameter / 2)
    .translate((0, 0, shaft_length / 2))
)

# Build the pan head (dome-like shape using revolve)
# Profile for pan head: flat bottom, rounded top
head = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(head_diameter / 2, 0)
    .threePointArc((head_diameter / 2 * 0.7, head_height * 0.9), (0, head_height))
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
    .translate((0, 0, shaft_length))
)

# Combine shaft and head
screw_body = shaft.union(head)

# Add thread approximation using a helical approach
# We'll simulate threads by cutting grooves using torus-like shapes stacked along shaft
# Use a series of small torus cuts to simulate threads
num_threads = int(shaft_length / thread_pitch)

# Create thread profile as a series of cuts
thread_cuts = None
for i in range(num_threads):
    z_pos = i * thread_pitch + thread_pitch / 2
    if z_pos > shaft_length - thread_pitch:
        break
    # Create a thin torus cut at each thread position
    torus = (
        cq.Workplane("XY")
        .workplane(offset=z_pos)
        .add(
            cq.CQ(
                cq.Solid.makeTorus(
                    shaft_diameter / 2,
                    thread_depth,
                )
            )
        )
    )
    if thread_cuts is None:
        thread_cuts = torus
    else:
        thread_cuts = thread_cuts.union(torus)

# Alternative simpler thread simulation: use cylinder with grooves
# Build threaded shaft by cutting grooves
threaded_shaft = (
    cq.Workplane("XY")
    .cylinder(shaft_length, shaft_diameter / 2)
    .translate((0, 0, shaft_length / 2))
)

# Cut thread grooves
for i in range(num_threads):
    z_pos = i * thread_pitch + thread_pitch / 2
    if z_pos >= shaft_length:
        break
    groove = (
        cq.Workplane("XY")
        .workplane(offset=z_pos)
        .circle(shaft_diameter / 2 + 0.01)
        .circle(shaft_diameter / 2 - thread_depth)
        .extrude(thread_pitch * 0.5, both=True)
    )
    # Use torus for groove
    torus_solid = cq.Solid.makeTorus(
        shaft_diameter / 2 - thread_depth / 2,
        thread_depth / 2 + 0.05,
    )
    torus_wp = cq.Workplane("XY").workplane(offset=z_pos).add(torus_solid)
    threaded_shaft = threaded_shaft.cut(torus_wp)

# Combine threaded shaft with head
result_body = threaded_shaft.union(head)

# Add Phillips head cross cut
cross_depth = head_height * 0.7
cross_width = 0.8
cross_length = head_diameter * 0.7

# Cut Phillips cross slots
slot1 = (
    cq.Workplane("XY")
    .workplane(offset=shaft_length + head_height - cross_depth / 2)
    .box(cross_length, cross_width, cross_depth)
)

slot2 = (
    cq.Workplane("XY")
    .workplane(offset=shaft_length + head_height - cross_depth / 2)
    .box(cross_width, cross_length, cross_depth)
)

result = result_body.cut(slot1).cut(slot2)