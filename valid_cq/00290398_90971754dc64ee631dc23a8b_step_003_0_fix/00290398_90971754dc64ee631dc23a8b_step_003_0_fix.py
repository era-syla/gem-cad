import cadquery as cq

# Parameters
flange_width = 140
flange_depth = 20
stem_width = 20
stem_height = 100
thickness = 6
hole_diameter = 6
flange_holes = 7
stem_holes = 6
hole_spacing = 20
stem_hole_offset = hole_spacing

# Build T‐shaped profile and extrude
result = (
    cq.Workplane("XY")
      .polyline([
          (-flange_width/2, 0),
          ( flange_width/2, 0),
          ( flange_width/2, -flange_depth),
          ( stem_width/2, -flange_depth),
          ( stem_width/2, -flange_depth - stem_height),
          (-stem_width/2, -flange_depth - stem_height),
          (-stem_width/2, -flange_depth),
          (-flange_width/2, -flange_depth)
      ])
      .close()
      .extrude(thickness)
      # Create holes on top face
      .faces(">Z").workplane()
      # Flange holes
      .pushPoints([
          (
              -hole_spacing*(flange_holes-1)/2 + i*hole_spacing,
              -flange_depth/2
          ) for i in range(flange_holes)
      ])
      # Stem holes
      .pushPoints([
          (
              0,
              -flange_depth - stem_hole_offset - i*hole_spacing
          ) for i in range(stem_holes)
      ])
      .hole(hole_diameter)
)

result