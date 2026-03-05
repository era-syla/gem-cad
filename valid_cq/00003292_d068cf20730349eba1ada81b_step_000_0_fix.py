import cadquery as cq

# Base plate with rounded front and flat back
# The base is roughly rectangular with semicircular front
base_width = 50
base_depth = 40
base_height = 8
corner_radius = 20

# Create the base shape - rectangular with rounded front corners
base = (
    cq.Workplane("XY")
    .moveTo(-base_width/2, -base_depth/2)
    .lineTo(base_width/2, -base_depth/2)
    .lineTo(base_width/2, 0)
    .threePointArc((0, base_depth/2), (-base_width/2, 0))
    .lineTo(-base_width/2, -base_depth/2)
    .close()
    .extrude(base_height)
)

# Add chamfers on the back corners
base = base.edges("|Z").edges(cq.selectors.BoxSelector(
    (-base_width/2 - 1, -base_depth/2 - 1, -1),
    (base_width/2 + 1, -base_depth/2 + 0.1, base_height + 1)
)).chamfer(5)

# Central cylinder boss
cylinder_od = 22
cylinder_id = 10
cylinder_height = 20

result = (
    base
    .faces(">Z")
    .workplane()
    .pushPoints([(0, 0)])
    .circle(cylinder_od / 2)
    .extrude(cylinder_height)
)

# Add the bore through the cylinder
result = (
    result
    .faces(">Z")
    .workplane()
    .circle(cylinder_id / 2)
    .cutBlind(-cylinder_height - base_height)
)

# Add small side bump/protrusion on the cylinder (visible on right side)
bump_radius = 4
bump_height = 3

result = (
    result
    .faces(">Z[-2]")
    .workplane()
    .center(cylinder_od/2 - 1, 0)
    .circle(bump_radius)
    .extrude(bump_height)
)

# Add mounting holes in the base (front left and front right area)
hole_radius = 3.5
hole_offset_x = 18
hole_offset_y = 8

result = (
    result
    .faces(">Z[-3]")
    .workplane()
    .pushPoints([(-hole_offset_x, hole_offset_y), (hole_offset_x, hole_offset_y)])
    .circle(hole_radius)
    .cutBlind(-base_height - 1)
)

# Add small bosses around the mounting holes
result = (
    result
    .faces(">Z[-3]")
    .workplane()
    .pushPoints([(-hole_offset_x, hole_offset_y), (hole_offset_x, hole_offset_y)])
    .circle(hole_radius + 2)
    .extrude(3)
)

# Re-drill the holes through the bosses
result = (
    result
    .faces(">Z[-3]")
    .workplane()
    .pushPoints([(-hole_offset_x, hole_offset_y), (hole_offset_x, hole_offset_y)])
    .circle(hole_radius)
    .cutBlind(-base_height - 5)
)