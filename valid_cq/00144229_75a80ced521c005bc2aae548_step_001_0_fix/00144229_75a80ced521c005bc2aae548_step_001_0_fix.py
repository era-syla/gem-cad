import cadquery as cq

# Parameters
length = 100
bf = 40          # flange width
tf = 5           # flange thickness
tw = 5           # web thickness
h_web = 60       # web height
plate_ov = 10    # plate overhang beyond flange
plate_thk = 5    # plate thickness
hole_d = 6       # hole diameter
hole_margin = 10 # margin from plate ends to hole center

# Compute hole offset from center
hole_offset = (length - 2*plate_ov)/2 - hole_margin

result = (
    # Create I-beam cross section and extrude along Y
    cq.Workplane("XZ")
      .polyline([
          (-bf/2, 0),
          ( bf/2, 0),
          ( bf/2, tf),
          ( tw/2, tf),
          ( tw/2, tf + h_web),
          ( bf/2, tf + h_web),
          ( bf/2, tf + h_web + tf),
          (-bf/2, tf + h_web + tf),
          (-bf/2, tf + h_web),
          (-tw/2, tf + h_web),
          (-tw/2, tf),
          (-bf/2, tf)
      ]).close()
      .extrude(length, both=True)
    # Add top plate
      .faces(">Z").workplane()
      .rect(bf + 2*plate_ov, length - 2*plate_ov)
      .extrude(plate_thk)
    # Drill two holes in the plate
      .faces(">Z").workplane()
      .pushPoints([(0,  hole_offset), (0, -hole_offset)])
      .hole(hole_d)
)

# 'result' holds the final model geometry.