import cadquery as cq

# --- Parametric Dimensions ---
# Base dimensions
base_dia = 12.0
base_height = 4.0

# First section (bottom thickest tube)
sec1_dia = 9.0
sec1_height = 40.0
collar1_dia = 9.6  # Slightly wider ring at the transition
collar1_height = 1.5

# Second section (middle tube)
sec2_dia = 6.0
sec2_height = 35.0
collar2_dia = 6.6
collar2_height = 1.5

# Third section (upper holder)
sec3_dia = 3.0
sec3_height = 15.0

# Tip (needle)
tip_dia = 0.8
tip_height = 30.0

# --- Modeling Process ---

# 1. Base
result = cq.Workplane("XY").circle(base_dia / 2.0).extrude(base_height)

# 2. First cylindrical section
result = (result.faces(">Z")
          .workplane()
          .circle(sec1_dia / 2.0)
          .extrude(sec1_height))

# 3. First transition collar
result = (result.faces(">Z")
          .workplane()
          .circle(collar1_dia / 2.0)
          .extrude(collar1_height))

# 4. Second cylindrical section
result = (result.faces(">Z")
          .workplane()
          .circle(sec2_dia / 2.0)
          .extrude(sec2_height))

# 5. Second transition collar
result = (result.faces(">Z")
          .workplane()
          .circle(collar2_dia / 2.0)
          .extrude(collar2_height))

# 6. Third cylindrical section (base for the tip)
result = (result.faces(">Z")
          .workplane()
          .circle(sec3_dia / 2.0)
          .extrude(sec3_height))

# 7. Antenna Tip
result = (result.faces(">Z")
          .workplane()
          .circle(tip_dia / 2.0)
          .extrude(tip_height))