import cadquery as cq

# --- Parametric Dimensions ---
plate_width = 20.0        # Width of the plate (and diameter of the rounded ends)
plate_thickness = 2.0     # Thickness of the extrusion
hole_diameter = 6.0       # Diameter of the 5 holes
num_holes = 5             # Total number of holes
hole_pitch = 20.0         # Distance between hole centers

# --- Derived Geometry Calculations ---
# Calculate the distance between the center of the first hole and the last hole
center_distance = (num_holes - 1) * hole_pitch

# Total length of the part (tip to tip)
# For a stadium shape with holes concentric to the ends, 
# total length = center_distance + plate_width (radius * 2)
total_length = center_distance + plate_width

# --- 3D Modeling ---

# 1. Create the base stadium shape
# slot2D creates a 2D slot/stadium profile. 
# angle=90 orients the length along the Y-axis to match the image orientation.
result = (
    cq.Workplane("XY")
    .slot2D(total_length, plate_width, angle=90)
    .extrude(plate_thickness)
)

# 2. Calculate hole coordinates
# The part is centered at (0,0,0). We generate points along the Y-axis.
hole_points = []
start_y = -center_distance / 2.0

for i in range(num_holes):
    y_pos = start_y + (i * hole_pitch)
    hole_points.append((0, y_pos))

# 3. Cut the holes through the plate
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(hole_points)
    .hole(hole_diameter)
)