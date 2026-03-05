import cadquery as cq
import math

# Parameters
head_diameter = 8.0
head_height = 3.2
shank_diameter = 4.0
shank_length = 12.0
thread_pitch = 0.7
thread_depth = 0.4

# Build the screw head (pan head shape)
head = (
    cq.Workplane("XY")
    .cylinder(head_height * 0.6, head_diameter / 2)
)

# Add domed top to head
dome = (
    cq.Workplane("XY")
    .workplane(offset=head_height * 0.6 - 0.1)
    .sphere(head_diameter / 2 * 0.85)
)

# Use a simpler approach: pan head as a revolved profile
# Profile: flat bottom, cylindrical sides with rounded top
head = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(head_diameter / 2, 0)
    .lineTo(head_diameter / 2, head_height * 0.7)
    .threePointArc(
        (head_diameter / 2 * 0.7, head_height),
        (0, head_height)
    )
    .close()
    .revolve(360, [0, 0, 0], [0, 1, 0])
)

# Build threaded shank using helix approximation with cylinders
# Main shank cylinder
shank = (
    cq.Workplane("XY")
    .workplane(offset=-shank_length)
    .circle(shank_diameter / 2)
    .extrude(shank_length)
)

# Combine head and shank
screw_body = head.union(shank)

# Add thread approximation using a helical groove
# Create thread ridges by adding a swept profile
# Approximate threads with stacked torus-like cuts
num_threads = int(shank_length / thread_pitch)

thread_result = screw_body

# Add Phillips head cross recess
# Two intersecting rectangular slots
slot_depth = 1.5
slot_width = 1.2
slot_length = head_diameter * 0.65

# Slot 1 - along X axis
slot1 = (
    cq.Workplane("XY")
    .workplane(offset=head_height - slot_depth + 0.5)
    .rect(slot_length, slot_width)
    .extrude(slot_depth + 1)
)

# Slot 2 - along Y axis (rotated 90 degrees)
slot2 = (
    cq.Workplane("XY")
    .workplane(offset=head_height - slot_depth + 0.5)
    .rect(slot_width, slot_length)
    .extrude(slot_depth + 1)
)

# Phillips recess shape - tapered
phillips_cut = (
    cq.Workplane("XY")
    .workplane(offset=head_height - slot_depth + 0.3)
    .rect(slot_length, slot_width)
    .workplane(offset=slot_depth)
    .rect(0.2, 0.2)
    .loft()
)

phillips_cut2 = (
    cq.Workplane("XY")
    .workplane(offset=head_height - slot_depth + 0.3)
    .rect(slot_width, slot_length)
    .workplane(offset=slot_depth)
    .rect(0.2, 0.2)
    .loft()
)

result = thread_result.cut(slot1).cut(slot2)

# Add thread approximation - use wire cuts around shank
# Create approximate threads as a series of thin disk cuts
thread_body = cq.Workplane("XY")

# Build thread profile by cutting helical groove approximation
# Use multiple angled cuts to simulate threading
z_start = -shank_length
for i in range(num_threads + 1):
    z_pos = z_start + i * thread_pitch
    if z_pos < 0 and z_pos > -shank_length:
        try:
            groove = (
                cq.Workplane("XY")
                .workplane(offset=z_pos)
                .circle(shank_diameter / 2 + thread_depth + 0.01)
                .circle(shank_diameter / 2 - thread_depth * 0.5)
                .extrude(thread_pitch * 0.45)
            )
            result = result.cut(
                cq.Workplane("XY")
                .workplane(offset=z_pos + thread_pitch * 0.25)
                .circle(shank_diameter / 2 + thread_depth * 0.1)
                .circle(shank_diameter / 2 - thread_depth * 0.8)
                .extrude(thread_pitch * 0.3)
            )
        except:
            pass

# Final result is already set
result = result