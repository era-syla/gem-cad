import cadquery as cq

# Parameters
base_radius = 45
inner_hole_radius = 20
thickness = 5
bolt_hole_radius = 3
bolt_circle_radius = 30
teeth_count = 60
tooth_depth = 5
tooth_width = 4

# Base disc
result = (
    cq.Workplane("XY")
      .circle(base_radius)
      .extrude(thickness)
      .faces(">Z")
      .workplane()
      .circle(inner_hole_radius)
      .cutBlind(thickness)
)

# Bolt holes
bolt_positions = [
    ( bolt_circle_radius,   0),
    (                0,   bolt_circle_radius),
    (-bolt_circle_radius,   0),
    (                0, -bolt_circle_radius)
]
result = (
    result
      .faces(">Z")
      .workplane()
      .pushPoints(bolt_positions)
      .circle(bolt_hole_radius)
      .cutBlind(thickness)
)

# Teeth
for i in range(teeth_count):
    angle = i * 360.0 / teeth_count
    tooth = (
        cq.Workplane("XY")
          .box(tooth_depth, tooth_width, thickness, centered=(False, True, False))
          .translate((base_radius, 0, 0))
          .rotate((0, 0, 0), (0, 0, 1), angle)
    )
    result = result.union(tooth)

# result holds the final gear geometry
result