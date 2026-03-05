import cadquery as cq

# Parameters
W = 40        # total width (X direction)
H_rect = 20   # rectangle height (Y direction)
thickness = 10  # extrusion thickness (Z direction)
R = W/2       # radius of the top semicircle
hole_dia = 15  # diameter of the pin hole

# Build the profile: bottom rectangle + top semicircle
result = (
    cq.Workplane("XY")
      .polyline([(-W/2, 0), (W/2, 0), (W/2, H_rect)])
      .threePointArc((0, H_rect + R), (-W/2, H_rect))
      .close()
      .extrude(thickness)
      # Drill the hole through the thickness
      .faces(">Z")
      .workplane(origin=(0, R/2))  # offset up so hole is centered in the semicircle region
      .hole(hole_dia)
)