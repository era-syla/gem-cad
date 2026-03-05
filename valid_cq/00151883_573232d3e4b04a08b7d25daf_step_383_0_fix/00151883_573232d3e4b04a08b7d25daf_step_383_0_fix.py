import cadquery as cq
import math

# Dimensions (adjust as needed)
h_bot1 = 2    # bottom small cylinder height
d_bot1 = 3    # bottom small cylinder diameter

h_bot2 = 4    # second cylinder height
d_bot2 = 5    # second cylinder diameter

h_mid_hex = 8            # middle hex prism height
hex_af_mid = 10          # middle hexagon across-flats

h_mid_cyl = 4    # cylinder above middle hex
d_mid_cyl = 6    # diameter of that cylinder

h_flange = 2     # flange thickness
d_flange = 12    # flange diameter

h_shaft = 20     # long shaft height
d_shaft = 8      # long shaft diameter

h_neck = 8       # neck above shaft
d_neck = 4       # neck diameter

h_top_hex = 6            # top hex prism height
hex_af_top = 6           # top hexagon across-flats

# Helper for hexagon circumscribed diameter
def hex_circum_diameter(across_flats):
    return across_flats / math.cos(math.pi/6)

# Build bottom small cylinder
result = cq.Workplane("XY").cylinder(h_bot1, d_bot1)

# Second cylinder
result = result.union(
    cq.Workplane("XY", origin=(0, 0, h_bot1))
      .cylinder(h_bot2, d_bot2)
)

# Middle hexagon prism
result = result.union(
    cq.Workplane("XY", origin=(0, 0, h_bot1 + h_bot2))
      .polygon(6, hex_circum_diameter(hex_af_mid))
      .extrude(h_mid_hex)
)

# Cylinder above middle hex
z3 = h_bot1 + h_bot2 + h_mid_hex
result = result.union(
    cq.Workplane("XY", origin=(0, 0, z3))
      .cylinder(h_mid_cyl, d_mid_cyl)
)

# Flange
z4 = z3 + h_mid_cyl
result = result.union(
    cq.Workplane("XY", origin=(0, 0, z4))
      .cylinder(h_flange, d_flange)
)

# Long shaft
z5 = z4 + h_flange
result = result.union(
    cq.Workplane("XY", origin=(0, 0, z5))
      .cylinder(h_shaft, d_shaft)
)

# Neck above shaft
z6 = z5 + h_shaft
result = result.union(
    cq.Workplane("XY", origin=(0, 0, z6))
      .cylinder(h_neck, d_neck)
)

# Top hexagon prism (acting like a hex nut/head)
z7 = z6 + h_neck
result = result.union(
    cq.Workplane("XY", origin=(0, 0, z7))
      .polygon(6, hex_circum_diameter(hex_af_top))
      .extrude(h_top_hex)
)

# Final result
result = result.translate((0, 0, 0))  # ensure result variable is set
