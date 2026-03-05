import cadquery as cq
import math

# Parameters
base_length = 50.0
base_width = 20.0
base_height = 8.0
hole_dist = 36.0
hole_dia = 4.0

neck_width = 10.0
neck_height = 20.0
neck_radius = 12.0

hook_outer_radius = 15.0
hook_inner_radius = 10.0
hook_center_z = base_height + neck_height + hook_outer_radius
hook_opening_angle = 60.0

# Base
result = cq.Workplane("XY").box(base_length, base_width, base_height)
result = result.edges("|Z").fillet(2.0)

# Holes in base
result = result.faces(">Z").workplane().pushPoints([(-hole_dist/2, 0), (hole_dist/2, 0)]).hole(hole_dia)

# Neck
neck_profile = (
    cq.Workplane("XZ")
    .workplane(offset=-base_width/2)
    .moveTo(-neck_width/2, base_height/2)
    .lineTo(neck_width/2, base_height/2)
    .lineTo(neck_width/2, base_height/2 + neck_height)
    .lineTo(-neck_width/2, base_height/2 + neck_height)
    .close()
    .extrude(base_width)
)

# Hook
hook_profile = (
    cq.Workplane("XZ")
    .workplane(offset=-base_width/2)
    .moveTo(0, hook_center_z)
    .circle(hook_outer_radius)
    .circle(hook_inner_radius)
    .extrude(base_width)
)

# Combine
result = result.union(neck_profile).union(hook_profile)

# Opening in hook
opening_box = (
    cq.Workplane("XZ")
    .workplane(offset=-base_width/2)
    .moveTo(hook_outer_radius, hook_center_z)
    .rect(hook_outer_radius*2, hook_outer_radius*2)
    .extrude(base_width)
)
# cut opening based on angle
cut_plane = (
    cq.Workplane("XZ")
    .workplane(offset=-base_width)
    .moveTo(0, hook_center_z)
    .lineTo(hook_outer_radius * 2 * math.cos(math.radians(hook_opening_angle)), 
            hook_center_z + hook_outer_radius * 2 * math.sin(math.radians(hook_opening_angle)))
    .lineTo(hook_outer_radius * 2, hook_center_z)
    .close()
    .extrude(base_width * 2)
)

result = result.cut(cut_plane)

# Fillets for smooth transitions
try:
    result = result.edges(cq.selectors.RadiusNthSelector(1)).fillet(2.0)
except:
    pass