import cadquery as cq

plate_thickness = 5
plate_diameter = 100
hole_diameter = 5
bolt_circle_diameter = 90
hole_count = 12

result = (
    cq.Workplane("XY")
      .circle(plate_diameter / 2)
      .extrude(plate_thickness)
      .faces(">Z")
      .workplane()
      .polarArray(bolt_circle_diameter / 2, 0, hole_count, 1)
      .circle(hole_diameter / 2)
      .cutThruAll()
)