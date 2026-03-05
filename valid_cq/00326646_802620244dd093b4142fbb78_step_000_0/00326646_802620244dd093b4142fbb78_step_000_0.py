import cadquery as cq

# Parametric dimensions
center_distance = 100.0  # Distance between the centers of the two holes
link_width = 25.0        # Width of the link (diameter of the rounded ends)
thickness = 5.0          # Thickness of the plate
hole_diameter = 10.0     # Diameter of the mounting holes

# Create the model
# 1. Start on XY plane
# 2. Create a 2D slot/stadium profile. 
#    - length is the center-to-center distance
#    - diameter is the width
#    - angle=90 orients the link along the Y-axis to match the image
# 3. Extrude to create the solid base
# 4. Select the top face to locate holes
# 5. Cut holes at the foci of the slot (centers)
result = (
    cq.Workplane("XY")
    .slot2D(center_distance, link_width, 90)
    .extrude(thickness)
    .faces(">Z")
    .workplane()
    .pushPoints([(0, -center_distance / 2), (0, center_distance / 2)])
    .hole(hole_diameter)
)