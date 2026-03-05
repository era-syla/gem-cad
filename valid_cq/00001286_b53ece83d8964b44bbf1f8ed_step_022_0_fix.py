import cadquery as cq
import math

# Parameters
bolt_diameter = 8.0
bolt_radius = bolt_diameter / 2
thread_diameter = bolt_diameter
shank_length = 30.0
thread_length = 20.0
total_length = shank_length + thread_length

# Bolt head (hex) parameters
head_hex_diameter = 14.0  # across flats
head_height = 5.0

# Washer parameters
washer_outer_diameter = 18.0
washer_inner_diameter = bolt_diameter + 0.5
washer_height = 2.0

# Nut parameters
nut_hex_diameter = 14.0  # across flats
nut_height = 7.0

# Thread approximation using helix-like profile
def make_threads(diameter, length, pitch=1.5, z_start=0):
    """Create approximate threads as a series of grooves"""
    thread_r = diameter / 2
    groove_depth = 0.4
    threads = []
    z = z_start
    while z < z_start + length - pitch:
        thread = (
            cq.Workplane("XY")
            .workplane(offset=z)
            .circle(thread_r)
            .workplane(offset=pitch/2)
            .circle(thread_r - groove_depth)
            .workplane(offset=pitch/2)
            .circle(thread_r)
            .loft()
        )
        threads.append(thread)
        z += pitch
    return threads

# --- Build bolt head (hexagonal) ---
hex_flat_to_flat = head_hex_diameter
hex_corner_to_corner = hex_flat_to_flat / math.cos(math.pi / 6)

bolt_head = (
    cq.Workplane("XY")
    .polygon(6, hex_corner_to_corner)
    .extrude(head_height)
)

# --- Build shank ---
shank = (
    cq.Workplane("XY")
    .workplane(offset=head_height)
    .circle(bolt_radius)
    .extrude(shank_length)
)

# --- Build threaded section (cylinder with thread approximation) ---
thread_section = (
    cq.Workplane("XY")
    .workplane(offset=head_height + shank_length)
    .circle(bolt_radius)
    .extrude(thread_length)
)

# Combine bolt parts
bolt_body = bolt_head.union(shank).union(thread_section)

# Add thread grooves
pitch = 1.5
groove_depth = 0.35
thread_r = bolt_radius
z_offset = head_height + shank_length
num_threads = int(thread_length / pitch)

for i in range(num_threads):
    z = z_offset + i * pitch
    groove = (
        cq.Workplane("XY")
        .workplane(offset=z)
        .circle(thread_r + 0.1)
        .workplane(offset=pitch * 0.3)
        .circle(thread_r - groove_depth)
        .workplane(offset=pitch * 0.4)
        .circle(thread_r - groove_depth)
        .workplane(offset=pitch * 0.3)
        .circle(thread_r + 0.1)
        .loft()
    )
    bolt_body = bolt_body.cut(groove)

# --- Washer ---
washer_z = head_height + shank_length * 0.3
washer = (
    cq.Workplane("XY")
    .workplane(offset=washer_z)
    .circle(washer_outer_diameter / 2)
    .circle(washer_inner_diameter / 2)
    .extrude(washer_height)
)

# --- Nut (hex with hole) ---
nut_corner_to_corner = nut_hex_diameter / math.cos(math.pi / 6)
nut_z = washer_z + washer_height

nut_outer = (
    cq.Workplane("XY")
    .workplane(offset=nut_z)
    .polygon(6, nut_corner_to_corner)
    .extrude(nut_height)
)

nut_hole = (
    cq.Workplane("XY")
    .workplane(offset=nut_z)
    .circle(bolt_radius + 0.2)
    .extrude(nut_height)
)

nut = nut_outer.cut(nut_hole)

# --- Combine everything ---
result = bolt_body.union(washer).union(nut)