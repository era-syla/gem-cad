import cadquery as cq

# Parametric dimensions for the Hex Standoff
# These values are estimates based on standard standoff proportions
hex_width = 6.0          # Flat-to-flat distance of the hexagon (e.g., M3 standoff usually has 5mm-6mm hex)
standoff_length = 30.0   # Length of the hexagonal body
thread_diameter = 3.0    # Diameter of the threaded sections (e.g., M3)
male_thread_length = 6.0 # Length of the male threaded stud
female_thread_depth = 8.0 # Depth of the female threaded hole

# Calculate the radius for the hexagon from the flat-to-flat distance
# For a hexagon, width (flat-to-flat) = sqrt(3) * radius (center-to-vertex)
# radius = width / sqrt(3)
# CadQuery's polygon uses the radius of the circumscribed circle (center-to-vertex).
import math
hex_radius = hex_width / math.sqrt(3)

# 1. Create the main hexagonal body
# We extrude a hexagon.
body = (cq.Workplane("XY")
        .polygon(6, hex_radius * 2) # polygon takes the diameter of the circumcircle
        .extrude(standoff_length)
       )

# 2. Create the male threaded stud at one end
# We select the top face and extrude a cylinder.
male_stud = (body.faces(">Z")
             .workplane()
             .circle(thread_diameter / 2)
             .extrude(male_thread_length)
            )

# 3. Create the female threaded hole at the other end
# We select the bottom face (which is at Z=0) and cut a blind hole.
# Note: Since the body was extruded in +Z, the bottom face is at Z=0.
result = (male_stud.faces("<Z")
          .workplane()
          .hole(thread_diameter, female_thread_depth)
         )

# If you want to view the result in an editor like CQ-editor, this variable is used.
# result contains the final object.