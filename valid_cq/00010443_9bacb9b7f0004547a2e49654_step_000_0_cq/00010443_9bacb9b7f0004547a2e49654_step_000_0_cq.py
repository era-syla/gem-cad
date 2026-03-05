import cadquery as cq

# Parametric dimensions
length = 60.0
width = 25.0
thickness = 8.0

# Cylinder (boss) dimensions
boss_diameter = 16.0
boss_height = 12.0  # Height above the top face
boss_hole_diameter = 6.5

# Countersunk hole dimensions (left side)
hole_diameter = 8.0
countersink_diameter = 14.0
countersink_angle = 90.0

# Create the base rectangular plate
base = cq.Workplane("XY").box(length, width, thickness)

# Create the cylindrical boss on the right side
# We create a new workplane on the top face
# Position is offset from center towards the right
boss_offset = length / 4.0

result = (
    base.faces(">Z").workplane()
    # Add the boss on the right side
    .center(boss_offset, 0)
    .circle(boss_diameter / 2.0)
    .extrude(boss_height)
    # Cut the hole through the boss and the plate
    .faces(">Z").workplane()
    .circle(boss_hole_diameter / 2.0)
    .cutBlind(-(boss_height + thickness))
)

# Add the countersunk hole on the left side
# Position is offset from center towards the left
hole_offset = -length / 4.0

result = (
    result.faces(">Z[1]") # Select the top face of the base plate (not the boss)
    .workplane()
    .center(hole_offset, 0)
    .cskHole(hole_diameter, countersink_diameter, countersink_angle)
)