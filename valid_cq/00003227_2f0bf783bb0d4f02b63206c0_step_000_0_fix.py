import cadquery as cq
import math

# Parameters
outer_radius = 50
outer_thickness = 4
rim_width = 5
spoke_width = 6
spoke_height = 8
hub_radius = 8
hub_height = 10
hole_radius = 3.5
bolt_hole_radius = 1.5
num_rim_holes = 16
num_hub_bolts = 4

# Create outer rim (flat disk ring)
rim = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(outer_radius - rim_width)
    .extrude(outer_thickness)
)

# Create spokes - 4 spokes at 45-degree angles (diagonal cross pattern)
def make_spoke(angle_deg):
    angle = math.radians(angle_deg)
    length = outer_radius - rim_width - hub_radius
    # spoke goes from hub to rim
    spoke = (
        cq.Workplane("XY")
        .transformed(rotate=cq.Vector(0, 0, angle_deg))
        .box(length, spoke_width, spoke_height, centered=True)
        .translate((hub_radius + length/2, 0, spoke_height/2 - outer_thickness/2))
    )
    return spoke

# Build spokes at 45, 135, 225, 315 degrees (diagonal)
spokes = None
for angle in [45, 135, 225, 315]:
    rad = math.radians(angle)
    length = outer_radius - rim_width - hub_radius - 1
    cx = (hub_radius + length/2) * math.cos(rad)
    cy = (hub_radius + length/2) * math.sin(rad)
    
    spoke = (
        cq.Workplane("XY")
        .box(length, spoke_width, spoke_height)
        .rotate((0,0,0), (0,0,1), angle)
        .translate((cx, cy, spoke_height/2))
    )
    if spokes is None:
        spokes = spoke
    else:
        spokes = spokes.union(spoke)

# Create hub cylinder
hub = (
    cq.Workplane("XY")
    .cylinder(hub_height, hub_radius)
    .translate((0, 0, hub_height/2))
)

# Combine hub and spokes
hub_assembly = hub.union(spokes)

# Cut center hole through hub
hub_assembly = (
    hub_assembly
    .cut(
        cq.Workplane("XY")
        .cylinder(hub_height + 2, hole_radius)
        .translate((0, 0, hub_height/2))
    )
)

# Add hub bolt holes (4 small holes around hub)
for angle in [0, 90, 180, 270]:
    rad = math.radians(angle)
    bx = (hub_radius - 1.5) * math.cos(rad) * 1.4
    by = (hub_radius - 1.5) * math.sin(rad) * 1.4
    hub_assembly = hub_assembly.cut(
        cq.Workplane("XY")
        .cylinder(hub_height + 2, bolt_hole_radius)
        .translate((bx, by, hub_height/2))
    )

# Combine rim with hub assembly
result = rim.union(hub_assembly)

# Add rim bolt holes
for i in range(num_rim_holes):
    angle = 360.0 / num_rim_holes * i
    rad = math.radians(angle)
    bx = (outer_radius - rim_width/2) * math.cos(rad)
    by = (outer_radius - rim_width/2) * math.sin(rad)
    result = result.cut(
        cq.Workplane("XY")
        .cylinder(outer_thickness + 2, bolt_hole_radius)
        .translate((bx, by, outer_thickness/2))
    )