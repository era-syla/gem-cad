import cadquery as cq

# Define parameters
length = 150
bottom_flange_half = 6
bottom_thickness = 4
web_thickness = 4
web_height = 16
top_flange_half = 9
top_thickness = 4
hole_diameter = 3
top_hole_y = bottom_thickness + web_height/2 + top_thickness/2
bottom_hole_y = bottom_thickness/2

# Create profile and extrude
result = (
    cq.Workplane("XY")
      .polyline([
          (-bottom_flange_half, 0),
          ( bottom_flange_half, 0),
          ( bottom_flange_half, bottom_thickness),
          (  web_thickness/2, bottom_thickness),
          (  web_thickness/2, bottom_thickness + web_height),
          ( top_flange_half, bottom_thickness + web_height),
          ( top_flange_half, bottom_thickness + web_height + top_thickness),
          (-top_flange_half, bottom_thickness + web_height + top_thickness),
          (-top_flange_half, bottom_thickness + web_height),
          (-web_thickness/2, bottom_thickness + web_height),
          (-web_thickness/2, bottom_thickness),
          (-bottom_flange_half, bottom_thickness)
      ])
      .close()
      .extrude(length)
      # Drill through-holes on the right face
      .faces(">X")
      .workplane(centerOption="CenterOfMass")
      .pushPoints([(-4, bottom_hole_y), (4, bottom_hole_y), (-5, top_hole_y), (5, top_hole_y)])
      .hole(hole_diameter)
)