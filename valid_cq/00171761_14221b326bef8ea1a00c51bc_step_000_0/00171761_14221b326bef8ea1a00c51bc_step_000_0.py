import cadquery as cq

# Geometric parameters derived from visual estimation
radius_wide = 12.0     # Radius of top and bottom sections
radius_narrow = 10.0   # Radius of the middle shaft section
height_bottom = 20.0   # Height of the bottom base section
height_shaft = 140.0   # Height of the middle shaft section
height_top = 50.0      # Height of the top head section

# Create the 3D model by stacking cylinders
# 1. Base Cylinder
result = cq.Workplane("XY").circle(radius_wide).extrude(height_bottom)

# 2. Middle Shaft (extruded from the top face of the base)
result = (result.faces(">Z")
          .workplane()
          .circle(radius_narrow)
          .extrude(height_shaft))

# 3. Top Head (extruded from the top face of the shaft)
result = (result.faces(">Z")
          .workplane()
          .circle(radius_wide)
          .extrude(height_top))