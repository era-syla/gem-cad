import cadquery as cq

# --- Parameters ---
# Base Plate dimensions
plate_width = 40.0
plate_height = 40.0
plate_thickness = 5.0

# Hole configurations (relative to plate center)
hole_y_offset = 10.0       # Vertical distance from center (Up)
hole_z_offset = 10.0       # Horizontal distance from center (Left/Right)
small_hole_dia = 5.0
large_hole_dia = 10.0

# Shaft dimensions
shaft_diameter = 6.0
shaft_length = 60.0

# Head (Disc) dimensions
head_diameter = 30.0
head_thickness = 2.0

# --- Modeling ---

# 1. Create Base Plate
# We align the base on the YZ plane so the shaft extends along the X-axis.
result = cq.Workplane("YZ").rect(plate_width, plate_height).extrude(plate_thickness)

# 2. Create Holes
# We select the back face (at X=0) and cut forward.
# On the YZ workplane: Local X maps to Global Y (Up), Local Y maps to Global Z (Right).
# Small hole is Top-Left (+Y, -Z).
# Large hole is Top-Right (+Y, +Z).
result = (result.faces("<X").workplane()
          .pushPoints([(hole_y_offset, -hole_z_offset)])
          .circle(small_hole_dia / 2.0)
          .cutBlind(-plate_thickness)  # Cut through the thickness
          )

result = (result.faces("<X").workplane()
          .pushPoints([(hole_y_offset, hole_z_offset)])
          .circle(large_hole_dia / 2.0)
          .cutBlind(-plate_thickness)
          )

# 3. Create Shaft
# Select the front face of the plate (>X) and extrude the shaft.
result = (result.faces(">X").workplane()
          .circle(shaft_diameter / 2.0)
          .extrude(shaft_length))

# 4. Create Head
# Select the end face of the shaft and extrude the head disc.
result = (result.faces(">X").workplane()
          .circle(head_diameter / 2.0)
          .extrude(head_thickness))

# 5. Add Detail (Center circle on head)
# A shallow cut to represent the circular feature seen in the center of the head.
result = (result.faces(">X").workplane()
          .circle(shaft_diameter / 2.0)
          .cutBlind(-0.2))