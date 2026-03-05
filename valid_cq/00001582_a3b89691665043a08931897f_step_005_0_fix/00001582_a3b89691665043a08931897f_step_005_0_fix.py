import cadquery as cq

# Parameters
plate_size = 100
thickness = 8
central_hole_dia = 20
small_hole_dia = 5
small_hole_dist = 20
protrusion_width = 20
protrusion_depth = 5
protrusion_offsets = [-30, 30]

# Base plate
result = cq.Workplane("XY").box(plate_size, plate_size, thickness)

# Center and small holes on top face
result = (
    result.faces(">Z")
          .workplane()
          .hole(central_hole_dia)
          .pushPoints([
              ( small_hole_dist,  0),
              (-small_hole_dist,  0),
              ( 0,  small_hole_dist),
              ( 0, -small_hole_dist),
          ])
          .hole(small_hole_dia)
)

# Protrusions on X faces
for face_name in (">X", "<X"):
    for offset in protrusion_offsets:
        result = (
            result.faces(face_name)
                  .workplane()
                  .center(offset, 0)
                  .rect(protrusion_width, thickness)
                  .extrude(protrusion_depth)
        )

# Protrusions on Y faces
for face_name in (">Y", "<Y"):
    for offset in protrusion_offsets:
        result = (
            result.faces(face_name)
                  .workplane()
                  .center(offset, 0)
                  .rect(protrusion_width, thickness)
                  .extrude(protrusion_depth)
        )