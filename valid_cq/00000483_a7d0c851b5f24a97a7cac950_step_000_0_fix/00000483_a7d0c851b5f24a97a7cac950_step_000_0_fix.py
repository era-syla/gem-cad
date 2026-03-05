import cadquery as cq

# Turnbuckle / long threaded rod with central coupler
# Main dimensions
total_length = 200
rod_diameter = 4
thread_major_diameter = 5
coupler_length = 15
coupler_width = 8
coupler_height = 8

# Create the main rod (smooth shaft)
rod = cq.Workplane("XY").cylinder(total_length, rod_diameter / 2)

# Create threaded appearance on left rod section using thin discs (thread simulation)
thread_pitch = 1.5
thread_depth = 0.6
left_thread_length = 80
right_thread_length = 80

def add_threads(workplane, start_z, length, pitch, major_r, minor_r):
    result = workplane
    z = start_z
    while z <= start_z + length:
        result = result.union(
            cq.Workplane("XY")
            .transformed(offset=(0, 0, z))
            .circle(major_r)
            .extrude(pitch * 0.5)
        )
        z += pitch
    return result

# Build the rod first
base_rod = cq.Workplane("XY").cylinder(total_length, rod_diameter / 2)

# Add thread profiles on left side
left_start = -total_length / 2
right_start = total_length / 2 - right_thread_length

# Create threaded rod sections as cylinders with slight ridges
# Left threaded section
left_thread = cq.Workplane("XY")
for i in range(int(left_thread_length / thread_pitch)):
    z_pos = left_start + i * thread_pitch
    left_thread = left_thread.add(
        cq.Workplane("XY")
        .transformed(offset=(0, 0, z_pos + thread_pitch / 2))
        .circle(thread_major_diameter / 2)
        .extrude(thread_pitch * 0.6)
    )

# Right threaded section  
right_thread = cq.Workplane("XY")
for i in range(int(right_thread_length / thread_pitch)):
    z_pos = right_start + i * thread_pitch
    right_thread = right_thread.add(
        cq.Workplane("XY")
        .transformed(offset=(0, 0, z_pos + thread_pitch / 2))
        .circle(thread_major_diameter / 2)
        .extrude(thread_pitch * 0.6)
    )

# Build complete assembly
# Main rod cylinder
main_rod = cq.Workplane("XY").cylinder(total_length, rod_diameter / 2)

# Left threaded portion - slightly larger cylinder
left_threaded_cyl = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, left_start + left_thread_length / 2))
    .circle(thread_major_diameter / 2)
    .extrude(left_thread_length)
)

# Right threaded portion
right_threaded_cyl = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, right_start + right_thread_length / 2))
    .circle(thread_major_diameter / 2)
    .extrude(right_thread_length)
)

# Combine rod with threaded sections
full_rod = main_rod.union(left_threaded_cyl).union(right_threaded_cyl)

# Add thread grooves (cuts)
groove_rod = full_rod
for i in range(int(left_thread_length / thread_pitch)):
    z_pos = left_start + i * thread_pitch + thread_pitch * 0.3
    groove_rod = groove_rod.cut(
        cq.Workplane("XY")
        .transformed(offset=(0, 0, z_pos))
        .circle(rod_diameter / 2 + 0.1)
        .extrude(thread_pitch * 0.4)
    )

for i in range(int(right_thread_length / thread_pitch)):
    z_pos = right_start + i * thread_pitch + thread_pitch * 0.3
    groove_rod = groove_rod.cut(
        cq.Workplane("XY")
        .transformed(offset=(0, 0, z_pos))
        .circle(rod_diameter / 2 + 0.1)
        .extrude(thread_pitch * 0.4)
    )

# Central coupler (rectangular block)
coupler = (
    cq.Workplane("XY")
    .box(coupler_length, coupler_width, coupler_height)
)

# Combine everything
result = groove_rod.union(coupler)