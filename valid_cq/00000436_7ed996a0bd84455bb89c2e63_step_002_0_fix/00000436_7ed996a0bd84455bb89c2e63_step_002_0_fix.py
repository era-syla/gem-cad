import cadquery as cq
import math

# Piston dimensions
piston_radius = 40
piston_height = 45
crown_height = 8
skirt_height = 30

# Main piston body (cylinder)
result = (
    cq.Workplane("XY")
    .cylinder(piston_height, piston_radius)
)

# Add crown (top dome - slightly raised)
crown = (
    cq.Workplane("XY")
    .workplane(offset=piston_height/2)
    .circle(piston_radius)
    .extrude(crown_height)
)

result = result.union(crown)

# Piston ring grooves (3 grooves near top)
for i, z_pos in enumerate([piston_height/2 + crown_height - 5, 
                             piston_height/2 + crown_height - 11, 
                             piston_height/2 + crown_height - 17]):
    groove = (
        cq.Workplane("XY")
        .workplane(offset=z_pos)
        .circle(piston_radius + 1)
        .circle(piston_radius - 2)
        .extrude(2)
    )
    result = result.cut(groove)

# Cut the skirt sides to make piston skirt shape
# Cut two opposing sides of lower cylinder for skirt
skirt_cut_width = piston_radius * 0.4
skirt_cut_depth = piston_radius * 0.15
skirt_bottom = -piston_height/2

skirt_cut1 = (
    cq.Workplane("XY")
    .workplane(offset=skirt_bottom)
    .rect(skirt_cut_width * 2, piston_radius * 0.5)
    .extrude(skirt_height * 0.6)
    .translate((piston_radius - skirt_cut_depth/2, 0, 0))
)

result = result.cut(skirt_cut1)

skirt_cut2 = (
    cq.Workplane("XY")
    .workplane(offset=skirt_bottom)
    .rect(skirt_cut_width * 2, piston_radius * 0.5)
    .extrude(skirt_height * 0.6)
    .translate((-piston_radius + skirt_cut_depth/2, 0, 0))
)

result = result.cut(skirt_cut2)

# Hollow out the inside (piston is hollow)
inner_cut = (
    cq.Workplane("XY")
    .workplane(offset=skirt_bottom + 2)
    .circle(piston_radius - 5)
    .extrude(piston_height - 10)
)

result = result.cut(inner_cut)

# Wrist pin boss holes
pin_boss = (
    cq.Workplane("YZ")
    .workplane(offset=0)
    .circle(7)
    .extrude(piston_radius + 5)
    .translate((0, 0, -piston_height/2 + skirt_height * 0.35))
)

result = result.cut(pin_boss)

# Crown top features - valve reliefs (4 curved cutouts)
for angle in [45, 135, 225, 315]:
    rad = math.radians(angle)
    x_pos = 22 * math.cos(rad)
    y_pos = 22 * math.sin(rad)
    
    valve_relief = (
        cq.Workplane("XY")
        .workplane(offset=piston_height/2 + crown_height - 3)
        .circle(10)
        .extrude(5)
        .translate((x_pos, y_pos, 0))
    )
    result = result.cut(valve_relief)

# Center circle groove on crown
center_groove = (
    cq.Workplane("XY")
    .workplane(offset=piston_height/2 + crown_height - 1)
    .circle(14)
    .circle(12)
    .extrude(2)
)
result = result.cut(center_groove)

# Outer crown groove
outer_crown_groove = (
    cq.Workplane("XY")
    .workplane(offset=piston_height/2 + crown_height - 1)
    .circle(piston_radius - 1)
    .circle(piston_radius - 3)
    .extrude(2)
)
result = result.cut(outer_crown_groove)