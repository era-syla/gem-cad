import cadquery as cq
import math

# Parameters
shaft_diameter = 4.0
shaft_length = 8.0
head_diameter = 7.5
head_height = 3.0
thread_pitch = 0.7
thread_depth = 0.3

# Build the screw shaft
shaft = (
    cq.Workplane("XY")
    .circle(shaft_diameter / 2)
    .extrude(shaft_length)
)

# Build threaded appearance using helical cuts approximated by rings
threaded_shaft = shaft
for i in range(int(shaft_length / thread_pitch)):
    z = i * thread_pitch
    if z + thread_pitch <= shaft_length:
        threaded_shaft = (
            threaded_shaft
            .workplane(offset=z)
            .circle((shaft_diameter / 2) - thread_depth)
            .circle(shaft_diameter / 2 + 0.01)
            .extrude(thread_pitch / 2, combine="cut")
        )

# Simpler approach - create shaft with thread grooves as torus cuts
shaft = (
    cq.Workplane("XY")
    .circle(shaft_diameter / 2)
    .extrude(shaft_length)
)

# Add thread grooves as circular cuts at regular intervals
result = shaft
num_threads = int(shaft_length / thread_pitch)
for i in range(num_threads + 1):
    z_pos = i * thread_pitch
    if 0 < z_pos < shaft_length:
        groove = (
            cq.Workplane("XY")
            .workplane(offset=z_pos)
            .circle((shaft_diameter / 2) - thread_depth)
            .extrude(thread_pitch * 0.4)
        )
        # Create ring by subtracting inner from outer cylinder
        outer_ring = (
            cq.Workplane("XY")
            .workplane(offset=z_pos - thread_pitch * 0.2)
            .circle(shaft_diameter / 2 + 0.1)
            .extrude(thread_pitch * 0.4)
        )
        inner_ring = (
            cq.Workplane("XY")
            .workplane(offset=z_pos - thread_pitch * 0.2)
            .circle((shaft_diameter / 2) - thread_depth)
            .extrude(thread_pitch * 0.4)
        )
        cut_ring = outer_ring.cut(inner_ring)
        result = result.cut(cut_ring)

# Create pan head - dome shaped
# Use a sphere-cylinder combination for pan head
head_base = (
    cq.Workplane("XY")
    .workplane(offset=shaft_length)
    .circle(head_diameter / 2)
    .extrude(head_height * 0.4)
)

# Dome top using sphere
sphere_radius = head_diameter * 0.7
sphere_center_z = shaft_length + head_height * 0.4 - math.sqrt(max(0, sphere_radius**2 - (head_diameter/2)**2))

dome = (
    cq.Workplane("XY")
    .workplane(offset=sphere_center_z)
    .sphere(sphere_radius)
)

# Trim dome with cylinder
dome_cylinder = (
    cq.Workplane("XY")
    .workplane(offset=shaft_length + head_height * 0.4)
    .circle(head_diameter / 2)
    .extrude(sphere_radius)
)

dome_trimmed = dome.intersect(dome_cylinder)

head = head_base.union(dome_trimmed)
result = result.union(head)

# Phillips cross slot
slot_depth = head_height * 0.6
slot_width = 1.0
slot_length = head_diameter * 0.55
top_z = shaft_length + head_height * 0.4 + head_height * 0.6

# Cut cross slots for phillips head
slot1 = (
    cq.Workplane("XY")
    .workplane(offset=top_z - slot_depth)
    .rect(slot_width, slot_length)
    .extrude(slot_depth + 0.5)
)

slot2 = (
    cq.Workplane("XY")
    .workplane(offset=top_z - slot_depth)
    .rect(slot_length, slot_width)
    .extrude(slot_depth + 0.5)
)

# Center punch
punch = (
    cq.Workplane("XY")
    .workplane(offset=top_z - slot_depth)
    .rect(slot_width * 1.3, slot_width * 1.3)
    .extrude(slot_depth + 0.5)
)

result = result.cut(slot1).cut(slot2)