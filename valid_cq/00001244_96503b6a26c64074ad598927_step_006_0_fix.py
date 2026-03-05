import cadquery as cq

# Key blade - a flat metal key blank with a groove running along its length
# Overall dimensions: long thin flat piece

# Key blade parameters
total_length = 60.0
blade_width = 8.0
blade_thickness = 2.5
tip_width = 4.0

# Create the main blade body as a tapered flat piece
# The blade tapers from wider at the bow end to narrower at the tip

# Create main blade profile using vertices
blade_points = [
    (-30, -4),   # left side of bow end
    (-22, -4),   # bow area
    (-22, -2),   # step in at bow
    (-18, -2),   # 
    (-18, -4),   # back out
    (-15, -4),   # 
    (-15, 4),    # top of bow
    (-18, 4),    # 
    (-18, 2),    # step
    (-22, 2),    # 
    (-22, 4),    # 
    (-30, 4),    # top left
]

# Simpler approach: build the key blade from primitives

# Main rectangular blade body
blade = (
    cq.Workplane("XY")
    .box(55, blade_width, blade_thickness)
)

# Taper the tip - cut a wedge shape to narrow the tip
# The tip narrows from blade_width to tip_width over the last 20mm
tip_cut_amount = (blade_width - tip_width) / 2  # 2mm each side

# Cut top taper at tip
blade = (
    blade
    .faces(">Z")
    .workplane()
    .transformed(offset=cq.Vector(0, 0, 0))
)

# Use shell cutting approach - create tapered tip by boolean
tip_taper = (
    cq.Workplane("XY")
    .polyline([
        (27.5 - 20, blade_width/2 + 0.1),
        (27.5, blade_width/2 + 0.1),
        (27.5, tip_width/2),
        (27.5 - 20, blade_width/2 + 0.1),
    ])
    .close()
    .extrude(blade_thickness + 1, both=True)
)

tip_taper2 = (
    cq.Workplane("XY")
    .polyline([
        (27.5 - 20, -blade_width/2 - 0.1),
        (27.5, -blade_width/2 - 0.1),
        (27.5, -tip_width/2),
        (27.5 - 20, -blade_width/2 - 0.1),
    ])
    .close()
    .extrude(blade_thickness + 1, both=True)
)

blade = (
    cq.Workplane("XY")
    .box(55, blade_width, blade_thickness)
    .cut(tip_taper)
    .cut(tip_taper2)
)

# Add the bow (head) of the key - wider rectangular section at the left end
bow = (
    cq.Workplane("XY")
    .box(12, 12, blade_thickness)
    .translate((-27.5 + (-6), 0, 0))
)

# Notch cuts in bow for key head shape
bow_notch1 = (
    cq.Workplane("XY")
    .box(3, 3, blade_thickness + 1)
    .translate((-27.5 - 9, 4.5, 0))
)
bow_notch2 = (
    cq.Workplane("XY")
    .box(3, 3, blade_thickness + 1)
    .translate((-27.5 - 9, -4.5, 0))
)

full_body = blade.union(bow).cut(bow_notch1).cut(bow_notch2)

# Add longitudinal groove along the blade (key channel)
groove = (
    cq.Workplane("XY")
    .box(52, 1.5, 1.2)
    .translate((1.5, 0, 0))
)

# Cut the groove into the top face
result = full_body.cut(groove)

# Add small groove/channel recesses on sides
side_groove = (
    cq.Workplane("XY")
    .box(48, blade_width + 1, 0.8)
    .translate((1.5, 0, (blade_thickness/2) - 0.4))
)

# Round the tip
tip_round = (
    cq.Workplane("XY")
    .cylinder(blade_thickness * 2, tip_width/2)
    .rotate((0,0,0), (1,0,0), 90)
    .translate((27.5, 0, 0))
)

result = result.union(tip_round)

# Fillet some edges for realism
result = (
    result
    .edges("|Z")
    .fillet(0.3)
)