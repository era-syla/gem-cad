import cadquery as cq

# --- Parametric Dimensions ---
# Large Cylinder (Main Body)
large_cyl_radius = 11.0
large_cyl_length = 35.0

# Main Flange
main_flange_radius = 17.0
main_flange_thickness = 2.5

# Large Hexagon Section
large_hex_circum_dia = 26.0  # Diameter across corners
large_hex_thickness = 10.0

# Small Cylinder Shaft
shaft_radius = 5.5
shaft_length = 12.0

# Small Washer/Flange
small_flange_radius = 8.5
small_flange_thickness = 1.5

# Small Hexagon Head (Tip)
small_hex_circum_dia = 10.0
small_hex_thickness = 4.0

# --- Geometry Construction ---

# 1. Create the large cylinder extending in the +Z direction
# We start from the XY plane.
result = cq.Workplane("XY").circle(large_cyl_radius).extrude(large_cyl_length)

# 2. Create the Main Flange
# We select the bottom face (Z=0) of the cylinder. 
# Creating a workplane here with standard orientation means the normal points in -Z.
# Positive extrusion on this workplane adds material downwards.
result = result.faces("<Z").workplane() \
    .circle(main_flange_radius).extrude(main_flange_thickness)

# 3. Create the Large Hexagon Section
# Select the new bottom face and extrude the hexagon shape
result = result.faces("<Z").workplane() \
    .polygon(6, large_hex_circum_dia).extrude(large_hex_thickness)

# 4. Create the Small Cylinder Shaft
# Select the bottom face of the hexagon
result = result.faces("<Z").workplane() \
    .circle(shaft_radius).extrude(shaft_length)

# 5. Create the Small Flange/Washer
# Select the bottom face of the shaft
result = result.faces("<Z").workplane() \
    .circle(small_flange_radius).extrude(small_flange_thickness)

# 6. Create the Small Hexagon Head
# Select the bottom face of the small flange
result = result.faces("<Z").workplane() \
    .polygon(6, small_hex_circum_dia).extrude(small_hex_thickness)

# The 'result' variable now contains the complete solid model.