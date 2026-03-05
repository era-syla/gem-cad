import cadquery as cq
import math

# Parameters
head_diameter = 8.0
head_height = 2.5
head_dome_height = 1.5
shank_diameter = 4.0
shank_length = 16.0
thread_pitch = 0.8
thread_depth = 0.4

# Build the screw head (pan head style - flat bottom with domed top)
# Pan head: cylindrical base with rounded top
head = (
    cq.Workplane("XY")
    .circle(head_diameter / 2)
    .extrude(head_height)
)

# Add dome on top of head using a sphere cut approach
# Create a rounded top by revolving a profile
dome_radius = (head_diameter**2 / (8 * head_dome_height)) + head_dome_height / 2
dome_center_z = head_height + dome_radius - head_dome_height

# Create dome as intersection of sphere with cylinder region
dome_sphere = (
    cq.Workplane("XY")
    .workplane(offset=dome_center_z)
    .sphere(dome_radius)
)

# Keep only the part of dome above head top
dome_box = (
    cq.Workplane("XY")
    .workplane(offset=head_height)
    .box(head_diameter + 2, head_diameter + 2, head_dome_height * 2, centered=(True, True, False))
)

dome_part = dome_sphere.intersect(dome_box)

# Combine head cylinder with dome
screw_head = head.union(dome_part)

# Add the shank
shank = (
    cq.Workplane("XY")
    .workplane(offset=-shank_length)
    .circle(shank_diameter / 2)
    .extrude(shank_length)
)

result = screw_head.union(shank)

# Add simplified threads using a helical approach
# Since helix() doesn't exist, simulate threads with stacked torus-like cuts/additions
num_threads = int(shank_length / thread_pitch)
thread_z_start = -shank_length + thread_pitch / 2

thread_solid = cq.Workplane("XY")

# Build thread profile as small torus rings along the shank
thread_parts = []
for i in range(num_threads):
    z_pos = thread_z_start + i * thread_pitch
    if z_pos < -thread_pitch or z_pos > -thread_pitch / 2:
        # Create a torus-like thread ring
        # Revolve a small triangle profile
        outer_r = shank_diameter / 2 + thread_depth
        inner_r = shank_diameter / 2 - thread_depth * 0.2
        
        ring = (
            cq.Workplane("XZ")
            .workplane(offset=0)
            .transformed(offset=cq.Vector(0, 0, z_pos))
        )
        
        # Create thread ring as a torus approximation
        thread_ring = (
            cq.Workplane("XY")
            .workplane(offset=z_pos)
            .circle(outer_r)
            .extrude(thread_pitch * 0.5)
        )
        
        thread_core = (
            cq.Workplane("XY")
            .workplane(offset=z_pos)
            .circle(shank_diameter / 2 - 0.05)
            .extrude(thread_pitch * 0.5)
        )
        
        thread_ring = thread_ring.cut(thread_core)
        thread_parts.append(thread_ring)

# Union all thread rings
if thread_parts:
    threads_combined = thread_parts[0]
    for t in thread_parts[1:]:
        threads_combined = threads_combined.union(t)
    result = result.union(threads_combined)

# Phillips head cross cutout
cross_depth = head_height + head_dome_height * 0.7
cross_width = 1.0
cross_length = head_diameter * 0.55

# Main cross slots
slot1 = (
    cq.Workplane("XY")
    .workplane(offset=head_height + head_dome_height)
    .box(cross_length, cross_width, cross_depth, centered=(True, True, False))
    .translate((0, 0, -cross_depth))
)

slot2 = (
    cq.Workplane("XY")
    .workplane(offset=head_height + head_dome_height)
    .box(cross_width, cross_length, cross_depth, centered=(True, True, False))
    .translate((0, 0, -cross_depth))
)

result = result.cut(slot1).cut(slot2)