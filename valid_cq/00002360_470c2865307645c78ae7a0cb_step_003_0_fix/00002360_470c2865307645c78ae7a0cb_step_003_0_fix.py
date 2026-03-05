import cadquery as cq

# Parameters
base_d = 30
base_h = 60
plate_th = 5
lobe_r = 20
bolt_d = 8
bolt_h = 6
fillet_r = 2

lobe_centers = [(lobe_r, 0), (0, lobe_r), (-lobe_r, 0), (0, -lobe_r)]
bolt_positions = [(lobe_r, 0), (-lobe_r, 0)]

result = (
    cq.Workplane("XY")
      .circle(base_d/2).extrude(base_h)
      .faces(">Z").workplane()
      .pushPoints(lobe_centers).circle(lobe_r).extrude(plate_th)
      .edges(">Z").fillet(fillet_r)
      .faces(">Z").workplane()
      .pushPoints(bolt_positions).polygon(6, bolt_d).extrude(bolt_h)
)