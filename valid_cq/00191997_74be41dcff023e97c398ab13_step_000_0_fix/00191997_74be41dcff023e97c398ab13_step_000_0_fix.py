import cadquery as cq

# Define key parameters
length = 60
width = 6
height = 12
jaw_length = 20
jaw_width = 3
jaw_depth = 2
taper_length = 15

# Create the main body
main_body = (cq.Workplane("XY")
             .box(length, width, height))

# Define the jaw cutout profile
jaw_cutout = (cq.Workplane("YZ")
              .moveTo(0, height / 2)
              .lineTo(-jaw_length, jaw_depth)
              .lineTo(-jaw_length, -jaw_depth)
              .lineTo(0, -height / 2)
              .close()
              .extrude(width)
              .translate((length / 2 - jaw_length, 0, 0)))

# Cut the jaw profile out
main_body = main_body.cut(jaw_cutout)

# Add the jaw teeth
teeth = (cq.Workplane("XY")
         .workplane(offset=width / 2)
         .rect(jaw_length, jaw_width, forConstruction=True)
         .vertices()
         .rect(jaw_depth, jaw_depth)
         .extrude(jaw_width)
         .translate((length / 2 - jaw_length / 2, 0, height / 2 - jaw_depth / 2)))

# Cut the teeth pattern
main_body = main_body.cut(teeth)

# Add the tapered handle end
tapered_end = (cq.Workplane("YZ")
               .moveTo(0, height / 2)
               .lineTo(taper_length, 0)
               .lineTo(0, -height / 2)
               .close()
               .extrude(width)
               .translate((-length / 2, 0, 0)))

# Subtract the tapered end
main_body = main_body.cut(tapered_end)

# Final result
result = main_body
