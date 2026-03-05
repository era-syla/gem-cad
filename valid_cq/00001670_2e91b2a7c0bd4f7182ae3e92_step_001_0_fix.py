import cadquery as cq
import math

# Screw parameters
head_diameter = 8.0
head_height = 2.5
shaft_diameter = 4.0
shaft_length = 10.0
thread_pitch = 1.0
thread_depth = 0.4

# Create the flat countersunk head (frustum shape)
# The head is a countersunk (flat/oval) head - wider at top, tapers to shaft diameter
head = (
    cq.Workplane("XY")
    .workplane(offset=shaft_length)
    .circle(head_diameter / 2)
    .workplane(offset=head_height)
    .circle(head_diameter / 2)
    .loft()
)

# Actually build head as a revolved profile
# Countersunk head profile: flat top, angled sides tapering down to shaft
head_profile = (
    cq.Workplane("XZ")
    .moveTo(0, shaft_length)
    .lineTo(head_diameter / 2, shaft_length)
    .lineTo(head_diameter / 2, shaft_length + 0.5)
    .lineTo(shaft_diameter / 2, shaft_length + head_height)
    .lineTo(0, shaft_length + head_height)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)

# Create shaft (cylinder)
shaft = (
    cq.Workplane("XY")
    .circle(shaft_diameter / 2)
    .extrude(shaft_length)
)

# Combine head and shaft
screw_body = shaft.union(head_profile)

# Add threads using helical approximation with stacked torus cuts
# Create thread profile by cutting grooves
thread_body = screw_body

# Add thread details - create a series of grooves to simulate threading
num_threads = int(shaft_length / thread_pitch)
for i in range(num_threads):
    z_pos = i * thread_pitch + thread_pitch / 2
    if z_pos < shaft_length - thread_pitch / 2:
        thread_body = (
            thread_body
            .cut(
                cq.Workplane("XY")
                .workplane(offset=z_pos)
                .circle(shaft_diameter / 2 + thread_depth)
                .circle(shaft_diameter / 2 - thread_depth)
                .extrude(thread_pitch * 0.4)
            )
        )

# Create a simpler threaded shaft using revolve
# Build complete screw from scratch with proper geometry

# Shaft with thread grooves approximated
base_shaft = (
    cq.Workplane("XY")
    .circle(shaft_diameter / 2)
    .extrude(shaft_length)
)

# Add countersunk head
head_solid = (
    cq.Workplane("XZ")
    .moveTo(shaft_diameter / 2, shaft_length)
    .lineTo(head_diameter / 2, shaft_length)
    .lineTo(head_diameter / 2, shaft_length + 0.3)
    .lineTo(shaft_diameter / 2, shaft_length + head_height)
    .lineTo(0, shaft_length + head_height)
    .lineTo(0, shaft_length)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)

screw = base_shaft.union(head_solid)

# Add Phillips head cross cutout
cross_width = 0.8
cross_depth = 1.5
cross_length = head_diameter * 0.6

cross1 = (
    cq.Workplane("XY")
    .workplane(offset=shaft_length + head_height - cross_depth)
    .rect(cross_width, cross_length)
    .extrude(cross_depth + 0.1)
)

cross2 = (
    cq.Workplane("XY")
    .workplane(offset=shaft_length + head_height - cross_depth)
    .rect(cross_length, cross_width)
    .extrude(cross_depth + 0.1)
)

screw = screw.cut(cross1).cut(cross2)

# Add thread grooves on shaft
for i in range(1, num_threads + 1):
    z_pos = i * thread_pitch
    if z_pos <= shaft_length - 0.5:
        groove = (
            cq.Workplane("XZ")
            .moveTo(shaft_diameter / 2 - thread_depth, z_pos - thread_pitch * 0.2)
            .lineTo(shaft_diameter / 2 + thread_depth * 0.8, z_pos)
            .lineTo(shaft_diameter / 2 - thread_depth, z_pos + thread_pitch * 0.2)
            .close()
            .revolve(360, (0, 0, 0), (0, 1, 0))
        )
        screw = screw.cut(groove)

result = screw