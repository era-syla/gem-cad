import cadquery as cq

# -- Parameters --
plate_length = 100.0  # Total length of the plate
plate_width = 60.0    # Total width of the plate
plate_thickness = 5.0 # Thickness of the plate

hole_diameter = 6.0   # Diameter of the 4 holes
hole_spacing_x = 70.0 # Distance between holes along the length
hole_spacing_y = 35.0 # Distance between holes along the width

# -- Modeling --

# 1. Create the base plate centered at the origin
result = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# 2. Add the holes
# We use rect() to create a set of points for the hole centers, 
# then circle() and cutThruAll() to remove the material.
result = (result
          .faces(">Z")
          .workplane()
          .rect(hole_spacing_x, hole_spacing_y, forConstruction=True)
          .vertices()
          .hole(hole_diameter)
          )

# The variable 'result' now contains the final geometry.