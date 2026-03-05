import cadquery as cq
import math

# This looks like a ratchet wrench or similar tool
# It has a long thin handle, a cylindrical body with a 90-degree bend, and a hook/pawl at the end

# Parameters
handle_radius = 3
handle_length = 80
body_radius = 6
body_length = 30
bend_radius = 10
hook_radius = 3
hook_length = 15

# Create the long thin handle (extending to the left/back)
handle = (
    cq.Workplane("XY")
    .circle(handle_radius)
    .extrude(handle_length)
)

# Create the main cylindrical body (larger cylinder)
body = (
    cq.Workplane("XY")
    .workplane(offset=handle_length)
    .circle(body_radius)
    .extrude(body_length)
)

# Combine handle and body
result = handle.union(body)

# Create the 90-degree bend section going upward
# The bend connects the body to a vertical section
bend_center_z = handle_length + body_length
bend_center_x = bend_radius

# Create a torus-like quarter for the bend
# Use a swept path approach
# Create path for the bend (quarter circle)
bend_path = (
    cq.Workplane("XZ")
    .moveTo(0, bend_center_z)
    .radiusArc((bend_radius, bend_center_z + bend_radius), -bend_radius)
)

bend_profile = (
    cq.Workplane("XY")
    .workplane(offset=bend_center_z)
    .circle(body_radius)
)

# Build the bent section using a swept approach manually
# Quarter torus for the bend
# Create it as a rotated sweep
bend = (
    cq.Workplane("XZ")
    .center(bend_radius, bend_center_z + bend_radius)
    .circle(body_radius)
)

# Use a different approach: create the bend as a rotational solid
# Sweep a circle along a quarter-circle path
path_wire = (
    cq.Workplane("XZ")
    .moveTo(0, bend_center_z)
    .threePointArc((bend_radius * (1 - math.cos(math.pi/4)), 
                    bend_center_z + bend_radius * math.sin(math.pi/4)),
                   (bend_radius, bend_center_z + bend_radius))
)

sweep_profile = cq.Workplane("XY").workplane(offset=bend_center_z).circle(body_radius)
bend_solid = sweep_profile.sweep(path_wire)

result = result.union(bend_solid)

# Create vertical section after the bend
vertical_section = (
    cq.Workplane("XY")
    .workplane(offset=bend_center_z + bend_radius)
    .center(bend_radius, 0)
    .circle(body_radius)
    .extrude(body_length * 0.8)
)

result = result.union(vertical_section)

# Create the hook at the top
hook_top_z = bend_center_z + bend_radius + body_length * 0.8
hook_bend_radius = 6

# Small bend for the hook
hook_path = (
    cq.Workplane("YZ")
    .moveTo(0, hook_top_z)
    .threePointArc(
        (hook_bend_radius * math.sin(math.pi/4), hook_top_z + hook_bend_radius * (1 - math.cos(math.pi/4))),
        (hook_bend_radius, hook_top_z + hook_bend_radius)
    )
)

hook_profile = (
    cq.Workplane("XY")
    .workplane(offset=hook_top_z)
    .center(bend_radius, 0)
    .circle(hook_radius)
)

hook_solid = hook_profile.sweep(hook_path)
result = result.union(hook_solid)

# Add a small cylinder tip for the hook end
hook_tip = (
    cq.Workplane("XZ")
    .workplane(offset=bend_radius + hook_bend_radius)
    .center(0, hook_top_z + hook_bend_radius)
    .circle(hook_radius)
    .extrude(hook_length)
)

result = result.union(hook_tip)