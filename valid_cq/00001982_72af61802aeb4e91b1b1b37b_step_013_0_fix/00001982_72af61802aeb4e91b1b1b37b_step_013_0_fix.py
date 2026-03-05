import cadquery as cq

# Parameters
base_width = 10
base_thickness = 10
base_half_length = 50

foot_length = 10
foot_width = 10
foot_height = 5
foot_positions = [-15, 15]

boss_radius = 5
boss_height = 5
hole_diameter = 3
hole_depth = base_thickness + boss_height

# Create the main lever body with a rounded left end and square right end
result = (
    cq.Workplane("XY")
      .moveTo(-45, -base_width/2)
      .threePointArc((-50, 0), (-45, base_width/2))
      .lineTo(base_half_length, base_width/2)
      .lineTo(base_half_length, -base_width/2)
      .close()
      .extrude(base_thickness)
)

# Add the two feet on the bottom
for x in foot_positions:
    foot = (
        cq.Workplane("XY")
          .transformed(offset=(x, 0, 0))
          .rect(foot_length, foot_width)
          .extrude(-foot_height)
    )
    result = result.union(foot)

# Create the pivot boss with a through hole
boss = (
    cq.Workplane("XY")
      .transformed(offset=(0, 0, base_thickness))
      .circle(boss_radius)
      .extrude(boss_height)
      .faces(">Z")
      .workplane()
      .hole(hole_diameter, depth=hole_depth)
)
result = result.union(boss)