import cadquery as cq

# Parametric dimensions
plate_diameter = 100.0  # Diameter of the main circular plate
plate_thickness = 5.0   # Thickness of the plate
hole_diameter = 8.0     # Diameter of the bolt holes
hole_circle_dia = 80.0  # Diameter of the circle on which holes are placed (PCD)
num_holes = 3           # Number of holes

# Create the main circular plate
# 1. Start with a workplane (XY plane is standard)
# 2. Draw a circle for the outer diameter
# 3. Extrude it to create the disk
result = (
    cq.Workplane("XY")
    .circle(plate_diameter / 2.0)
    .extrude(plate_thickness)
)

# Add the holes
# 1. Select the top face of the plate
# 2. Create a polar array for positioning the holes
#    - radius = hole_circle_dia / 2
#    - startAngle = 0 (or adjust to rotate the pattern)
#    - angle = 360 (full circle)
#    - count = num_holes
# 3. Draw the circles for the holes
# 4. Cut the holes through the plate
result = (
    result.faces(">Z")
    .workplane()
    .polarArray(hole_circle_dia / 2.0, 90, 360, num_holes) # Starting at 90 deg makes top hole centered
    .circle(hole_diameter / 2.0)
    .cutThruAll()
)