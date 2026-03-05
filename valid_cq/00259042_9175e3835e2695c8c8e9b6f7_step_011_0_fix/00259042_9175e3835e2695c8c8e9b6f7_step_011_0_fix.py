import cadquery as cq

# Parameters
L = 100    # total length
w = 20     # width
h = 10     # thickness
hole_d = 8 # hole diameter
r = w / 2  # end radius
y1 = L/2 - r

result = (
    cq.Workplane("XY")
      .moveTo(-w/2,  y1)
      .lineTo(-w/2, -y1)
      .threePointArc((0, -L/2), ( w/2, -y1))
      .lineTo( w/2,  y1)
      .threePointArc((0,  L/2), (-w/2,  y1))
      .close()
      .extrude(h)
      .faces(">Z")
      .workplane()
      .pushPoints([(0,  L/2 - r), (0, -L/2 + r)])
      .hole(hole_d)
)