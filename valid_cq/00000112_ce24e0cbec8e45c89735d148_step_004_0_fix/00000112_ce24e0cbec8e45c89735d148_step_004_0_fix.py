import cadquery as cq
import math

# Parameters
outer_radius = 10.0
length = 14.0
thread_pitch = 2.0
thread_depth = 1.2
inner_radius = 4.0
slot_width = 2.5
slot_depth = 3.0

# Create the main cylinder body
result = cq.Workplane("XY").cylinder(length, outer_radius)

# Add threads by creating helical grooves
# We'll approximate threads by subtracting rotated torus-like shapes
num_threads = int(length / thread_pitch)

# Create thread profile using a series of cuts along a helix approximation
# Build the threaded cylinder using a swept approach
# First create base cylinder
base = cq.Workplane("XY").cylinder(length, outer_radius)

# Create inner bore
base = base.faces(">Z").workplane().circle(inner_radius).cutThruAll()

# Create slot on top face (hex socket or flat slot)
base = (base
    .faces(">Z")
    .workplane()
    .rect(slot_width, outer_radius * 2.2)
    .cutBlind(-slot_depth)
)

# Now add thread grooves - approximate with angled cuts around the cylinder
# Use a series of torus cuts positioned along the helix
thread_result = base

# Create thread groove shape by cutting with a small profile swept around
# We'll use the workplane approach to cut thread-like grooves
for i in range(num_threads + 1):
    z_pos = -length / 2 + i * thread_pitch
    # Create a torus-like cut at slight angle to simulate thread
    angle_offset = (i % 1) * 360  # rotation per thread
    thread_result = (thread_result
        .workplane(offset=z_pos + length/2 - length/2, origin=(0, 0, z_pos))
        .transformed(offset=(0, 0, 0))
    )

# Rebuild with cleaner approach
result = cq.Workplane("XY").cylinder(length, outer_radius)

# Hollow center
result = result.faces(">Z").workplane().circle(inner_radius).cutBlind(-length * 0.8)

# Cut slot on top
result = (result
    .faces(">Z")
    .workplane()
    .rect(slot_width, outer_radius * 2.1)
    .cutBlind(-slot_depth)
)

# Add thread grooves using angled disc cuts
thread_wire_points = []
steps = 120
for i in range(steps + 1):
    angle = (i / steps) * 2 * math.pi * (length / thread_pitch)
    z = -length / 2 + (i / steps) * length
    x = (outer_radius - thread_depth / 2) * math.cos(angle / (length / thread_pitch))
    y = (outer_radius - thread_depth / 2) * math.sin(angle / (length / thread_pitch))

# Create thread grooves as a series of small torus cuts
for i in range(num_threads + 2):
    z_center = -length / 2 + (i - 0.5) * thread_pitch
    if abs(z_center) <= length / 2 + thread_pitch:
        try:
            cut_torus = (cq.Workplane("XY")
                .transformed(offset=cq.Vector(0, 0, z_center))
                .parametricCurve(
                    lambda t: (
                        (outer_radius + 0.3) * math.cos(t * 2 * math.pi),
                        (outer_radius + 0.3) * math.sin(t * 2 * math.pi),
                        0
                    )
                )
            )
        except:
            pass

# Final result: cylinder with bore and slot, thread grooves approximated
# by creating a wire-frame helix cut using revolve
groove_profile = (cq.Workplane("XZ")
    .moveTo(outer_radius - thread_depth, 0)
    .lineTo(outer_radius + 0.1, -thread_pitch * 0.4)
    .lineTo(outer_radius + 0.1, thread_pitch * 0.4)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)

# Position and subtract groove copies
for i in range(num_threads + 1):
    z_pos = -length / 2 + i * thread_pitch
    groove_inst = groove_profile.translate((0, 0, z_pos))
    result = result.cut(groove_inst)

result = result