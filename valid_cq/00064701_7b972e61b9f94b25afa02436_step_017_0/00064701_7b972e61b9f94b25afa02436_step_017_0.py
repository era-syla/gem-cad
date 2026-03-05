import cadquery as cq
import math

# --- Parametric Dimensions ---
# Define the dimensions of the part (in mm)
total_length = 60.0       # Total length of the standoff
hex_length = 12.0         # Length of the central hexagonal section
cyl_od = 8.0              # Outer diameter of the cylindrical ends
hex_width_across_flats = 10.0  # Width of the hex section (wrench size)
bore_diameter = 4.0       # Diameter of the central through-hole

# --- Derived Dimensions ---
# Calculate the length of the cylindrical sections
cyl_arm_length = (total_length - hex_length) / 2.0
# Calculate the circumscribed diameter of the hexagon based on the width across flats
# Formula: d = w / cos(30) = w / (sqrt(3)/2)
hex_circum_diameter = hex_width_across_flats / (math.sqrt(3) / 2.0)

# --- 3D Modeling ---

# 1. Create the central hexagonal section
# We orient the part along the X-axis. 
# extrude(..., both=True) creates the shape centered at the origin.
result = (
    cq.Workplane("YZ")
    .polygon(6, hex_circum_diameter)
    .extrude(hex_length / 2.0, both=True)
)

# 2. Add the cylindrical extension to the positive X side
result = (
    result
    .faces(">X")            # Select the face at the extreme positive X direction
    .workplane()
    .circle(cyl_od / 2.0)
    .extrude(cyl_arm_length)
)

# 3. Add the cylindrical extension to the negative X side
result = (
    result
    .faces("<X")            # Select the face at the extreme negative X direction
    .workplane()            # Normal of this workplane points in -X
    .circle(cyl_od / 2.0)
    .extrude(cyl_arm_length)# Positive extrusion goes outward (along normal)
)

# 4. Cut the central hole through the entire assembly
result = (
    result
    .faces(">X")            # Select the end face
    .workplane()
    .circle(bore_diameter / 2.0)
    .cutThruAll()           # Cut through the entire length of the solid
)