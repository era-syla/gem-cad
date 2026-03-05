import cadquery as cq

# Dimensions
outer_diameter = 60.0
inner_hole_diameter = 30.0
height = 15.0
wall_thickness = 4.0
floor_thickness = 4.0
boss_diameter = 12.0
boss_length = 15.0
boss_hole_diameter = 6.0

# 1. Create the main cylindrical body
result = cq.Workplane("XY").circle(outer_diameter / 2.0).extrude(height)

# 2. Cut the central through-hole
result = result.faces(">Z").workplane().circle(inner_hole_diameter / 2.0).cutThruAll()

# 3. Create the annular channel (recess)
# Calculate radii for the cut to leave inner and outer walls
recess_outer_radius = (outer_diameter / 2.0) - wall_thickness
recess_inner_radius = (inner_hole_diameter / 2.0) + wall_thickness
recess_depth = height - floor_thickness

result = (
    result.faces(">Z")
    .workplane()
    .circle(recess_outer_radius)
    .circle(recess_inner_radius)
    .cutBlind(-recess_depth)
)

# 4. Create and attach the side boss
# Create a workplane tangent to the outer surface (offset by radius)
# Center it vertically relative to the main body height
boss_plane = (
    cq.Workplane("YZ")
    .workplane(offset=outer_diameter / 2.0)
    .center(0, height / 2.0)
)

boss = boss_plane.circle(boss_diameter / 2.0).extrude(boss_length)
result = result.union(boss)

# 5. Drill the hole through the boss and the outer wall
# Select the furthest X face (tip of the boss) and cut inwards
# Distance must cover boss length + wall thickness + clearance to enter the channel
cut_distance = boss_length + wall_thickness + 2.0

result = (
    result.faces(">X")
    .workplane()
    .circle(boss_hole_diameter / 2.0)
    .cutBlind(-cut_distance)
)