import cadquery as cq
import math

# Socket head cap screw
# Parameters
head_diameter = 8.0
head_height = 5.0
shank_diameter = 5.0
shank_length = 20.0
thread_pitch = 1.0
thread_depth = 0.4

# Build the screw body
# Head (cylindrical)
head = (
    cq.Workplane("XY")
    .circle(head_diameter / 2)
    .extrude(head_height)
)

# Shank (smooth cylinder below threads, transitioning to threaded portion)
shank = (
    cq.Workplane("XY")
    .workplane(offset=head_height)
    .circle(shank_diameter / 2)
    .extrude(shank_length)
)

result = head.union(shank)

# Add thread simulation using a helix-like approach
# We'll simulate threads by cutting a helical groove using rotated ellipses stacked
# Use a series of torus-like cuts to simulate thread profile

# Number of thread turns
num_turns = int(shank_length / thread_pitch)

# Create thread profile by sweeping along a helix
# Since helix/sweep with helix is complex, we'll use a series of disc cuts

# Build thread as union of a slightly larger cylinder with grooves cut in
# Use parametric approach: create thread by cutting grooves

# Create the threaded section as a separate solid then union
# Build helix path manually using a wire

import cadquery as cq
from cadquery import Edge, Wire, Vector

# Redefine cleanly
head_d = 8.0
head_h = 5.0
shaft_d = 5.0
shaft_l = 20.0
pitch = 1.5
thread_h = 0.5  # thread tooth height
n_turns = shaft_l / pitch

# Head
result = (
    cq.Workplane("XY")
    .circle(head_d / 2)
    .extrude(head_h)
)

# Add chamfer on top edge of head
result = result.faces(">Z").chamfer(0.3)

# Shank base
result = (
    result
    .faces(">Z").wires().toPending()
    .workplane()
    .circle(shaft_d / 2)
    .extrude(shaft_l)
)

# Simulate threads by cutting helical grooves using stacked angled torus cuts
# We'll approximate with a series of groove cuts

thread_body = cq.Workplane("XY").workplane(offset=head_h)

# Create thread approximation: slightly larger cylinder minus groove rings
thread_outer = shaft_d / 2 + thread_h * 0.6
thread_inner = shaft_d / 2 - thread_h * 0.4

n_grooves = int(shaft_l / pitch) + 1

groove_solid = None
for i in range(n_grooves + 1):
    z_pos = head_h + i * pitch
    if z_pos > head_h + shaft_l:
        z_pos = head_h + shaft_l
    # Create a thin torus-like groove cut using a revolved profile
    groove = (
        cq.Workplane("XZ")
        .workplane(offset=0)
        .transformed(offset=cq.Vector(0, 0, z_pos))
        .polyline([
            (thread_outer, 0),
            (thread_inner, -pitch * 0.3),
            (thread_inner, pitch * 0.3),
            (thread_outer, 0)
        ])
        .close()
        .revolve(360, [0, 0, 0], [0, 0, 1])
    )
    if groove_solid is None:
        groove_solid = groove
    else:
        groove_solid = groove_solid.union(groove)

if groove_solid is not None:
    result = result.union(groove_solid)

# Final result
result = result