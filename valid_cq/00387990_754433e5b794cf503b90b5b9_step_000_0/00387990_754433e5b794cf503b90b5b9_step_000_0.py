import cadquery as cq

# Model parameters
cube_size = 20.0
hole_diameter = 6.0
pin_diameter = 5.0
pin_length = 3.0
arm_length = 30.0
arm_base_width = 7.0
arm_height = 7.0

# 1. Create the base cube centered at origin
result = cq.Workplane("XY").box(cube_size, cube_size, cube_size)

# 2. Create the hole on the top face
# Select the top face (+Z), create a workplane, and cut a hole
result = result.faces(">Z").workplane().hole(hole_diameter)

# 3. Create the cylindrical pin on the front-left face
# Select the front face (-Y), draw a circle, and extrude it outwards
result = (result.faces("<Y").workplane()
          .circle(pin_diameter / 2.0)
          .extrude(pin_length))

# 4. Create the triangular arm on the right face
# Select the right face (+X)
# Draw an inverted triangle (flat top, point down) to match the tip profile
# Extrude it along the normal
result = (result.faces(">X").workplane()
          .polyline([
              (-arm_base_width / 2.0, arm_height / 2.0),  # Top-left vertex
              (arm_base_width / 2.0, arm_height / 2.0),   # Top-right vertex
              (0.0, -arm_height / 2.0)                      # Bottom point vertex
          ])
          .close()
          .extrude(arm_length))