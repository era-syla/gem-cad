import cadquery as cq
import math

# Wheel rim parameters
outer_radius = 50
rim_width = 35
rim_thickness = 4
hub_radius = 8
hub_depth = 20
spoke_count = 10
spoke_width = 4
spoke_thickness = 3

# Create the outer rim shell by revolving a profile
rim_profile = (
    cq.Workplane("XZ")
    .moveTo(outer_radius - rim_thickness, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, rim_width)
    .lineTo(outer_radius - rim_thickness, rim_width)
    .lineTo(outer_radius - rim_thickness - 2, rim_width - 2)
    .lineTo(outer_radius - rim_thickness - 2, 2)
    .lineTo(outer_radius - rim_thickness, 0)
    .close()
)

rim = rim_profile.revolve(360, (0, 0, 0), (0, 1, 0))

# Create inner barrel/well of the rim
barrel_outer = outer_radius - rim_thickness - 2
barrel_inner = barrel_outer - 2

inner_barrel = (
    cq.Workplane("XZ")
    .moveTo(barrel_inner, 3)
    .lineTo(barrel_outer, 3)
    .lineTo(barrel_outer, rim_width - 3)
    .lineTo(barrel_inner, rim_width - 3)
    .close()
)
inner_barrel_solid = inner_barrel.revolve(360, (0, 0, 0), (0, 1, 0))

rim = rim.union(inner_barrel_solid)

# Create hub
hub = (
    cq.Workplane("YZ")
    .workplane(offset=0)
    .circle(hub_radius + 3)
    .extrude(hub_depth)
)

# Position hub in center of rim width
hub = hub.translate((0, rim_width / 2 - hub_depth / 2, 0))

rim = rim.union(hub)

# Create spokes
spoke_inner_r = hub_radius + 3
spoke_outer_r = barrel_inner

spoke_angle_step = 360.0 / spoke_count

spokes_solid = None

for i in range(spoke_count):
    angle = math.radians(i * spoke_angle_step)
    
    # Spoke direction vector
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    
    # Spoke center position
    mid_r = (spoke_inner_r + spoke_outer_r) / 2
    
    spoke = (
        cq.Workplane("XY")
        .box(
            spoke_outer_r - spoke_inner_r,
            spoke_thickness,
            spoke_width
        )
    )
    
    # Move to correct radial position
    spoke = spoke.translate((mid_r, 0, rim_width / 2))
    
    # Rotate around Z to correct angle
    spoke = spoke.rotate((0, 0, 0), (0, 0, 1), i * spoke_angle_step)
    
    if spokes_solid is None:
        spokes_solid = spoke
    else:
        spokes_solid = spokes_solid.union(spoke)

if spokes_solid is not None:
    rim = rim.union(spokes_solid)

# Add center hole in hub
center_hole = (
    cq.Workplane("YZ")
    .circle(4)
    .extrude(hub_depth + 5)
)
center_hole = center_hole.translate((0, rim_width / 2 - hub_depth / 2 - 1, 0))
rim = rim.cut(center_hole)

# Add bolt holes
bolt_circle_r = hub_radius - 1
bolt_hole_r = 1.5
bolt_count = 5

for i in range(bolt_count):
    angle = math.radians(i * 360.0 / bolt_count)
    bx = bolt_circle_r * math.cos(angle)
    bz = bolt_circle_r * math.sin(angle)
    
    bolt_hole = (
        cq.Workplane("YZ")
        .circle(bolt_hole_r)
        .extrude(hub_depth + 5)
    )
    bolt_hole = bolt_hole.translate((bx, rim_width / 2 - hub_depth / 2 - 1, bz))
    rim = rim.cut(bolt_hole)

# Add lip detail on rim edges
result = rim