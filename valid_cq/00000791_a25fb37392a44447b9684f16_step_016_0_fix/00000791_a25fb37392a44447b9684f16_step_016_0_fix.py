import cadquery as cq
import math

# Parameters
shaft_radius = 3.0
shaft_length = 30.0
head_radius = 5.5
head_height = 2.8
head_dome_height = 1.8

# Create the shaft (cylinder)
shaft = (
    cq.Workplane("XY")
    .cylinder(shaft_length, shaft_radius)
    .translate((0, 0, shaft_length / 2))
)

# Create thread grooves using a helical approach via repeated cuts
# We'll simulate threads by creating a series of torus-like cuts along the shaft
thread_result = (
    cq.Workplane("XY")
    .cylinder(shaft_length, shaft_radius)
)

# Add threads as surface grooves using revolve profiles
thread_pitch = 1.8
thread_depth = 0.5
num_threads = int(shaft_length / thread_pitch)

# Build threaded shaft by subtracting torus rings (approximate threads)
threaded_shaft = cq.Workplane("XY").cylinder(shaft_length, shaft_radius)

for i in range(num_threads + 1):
    z_pos = i * thread_pitch - shaft_length / 2 + thread_pitch / 2
    if -shaft_length / 2 < z_pos < shaft_length / 2:
        groove = (
            cq.Workplane("XY")
            .workplane(offset=z_pos)
            .circle(shaft_radius + thread_depth)
            .circle(shaft_radius - thread_depth * 0.3)
            .extrude(thread_pitch * 0.55, both=True)
        )
        # Use a torus-like cut
        torus_cut = (
            cq.Workplane("XZ")
            .workplane(offset=0)
            .transformed(offset=(0, z_pos, 0))
            .circle(thread_depth * 0.6)
            .revolve(360, (shaft_radius + thread_depth * 0.5, 0, 0), (shaft_radius + thread_depth * 0.5, 1, 0))
        )
        try:
            threaded_shaft = threaded_shaft.cut(torus_cut)
        except:
            pass

# Create the pan head (flat bottom + domed top)
head_base = (
    cq.Workplane("XY")
    .workplane(offset=shaft_length / 2)
    .circle(head_radius)
    .extrude(head_height)
)

# Dome on top of head using a sphere cut approach
dome_sphere_radius = (head_radius ** 2 + head_dome_height ** 2) / (2 * head_dome_height)
dome_center_z = shaft_length / 2 + head_height + dome_sphere_radius - head_dome_height

dome = (
    cq.Workplane("XY")
    .workplane(offset=dome_center_z)
    .sphere(dome_sphere_radius)
)

# Intersect dome with a cylinder to get just the cap portion
dome_cap_cyl = (
    cq.Workplane("XY")
    .workplane(offset=shaft_length / 2 + head_height - 0.01)
    .circle(head_radius)
    .extrude(head_dome_height + 1)
)

dome_cap = dome.intersect(dome_cap_cyl)

# Combine head parts
full_head = head_base.union(dome_cap)

# Combine shaft and head
result = threaded_shaft.union(full_head)

# Add Phillips head cross slot
slot_depth = 1.2
slot_width = 1.0
slot_length_val = head_radius * 0.85
slot_z = shaft_length / 2 + head_height + head_dome_height - slot_depth + 0.5

slot1 = (
    cq.Workplane("XY")
    .workplane(offset=slot_z)
    .rect(slot_width, slot_length_val * 2)
    .extrude(slot_depth + 1)
)

slot2 = (
    cq.Workplane("XY")
    .workplane(offset=slot_z)
    .rect(slot_length_val * 2, slot_width)
    .extrude(slot_depth + 1)
)

result = result.cut(slot1).cut(slot2)

# Add chamfer at tip of shaft
result = (
    result
    .faces("<Z")
    .edges()
    .chamfer(0.5)
)