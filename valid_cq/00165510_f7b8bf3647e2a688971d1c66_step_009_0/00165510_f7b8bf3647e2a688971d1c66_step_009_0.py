import cadquery as cq

# Parametric dimensions
plate_width = 120.0
plate_height = 50.0
plate_thickness = 2.0
hole_diameter = 1.5
hole_spacing = 6.0  # Distance between centers of adjacent holes

# Create the base rectangular plate centered at the origin
result = cq.Workplane("XY").box(plate_width, plate_height, plate_thickness)

# Define the points for the three horizontally aligned holes
hole_points = [
    (-hole_spacing, 0),
    (0, 0),
    (hole_spacing, 0)
]

# Cut the holes through the plate
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(hole_points)
    .hole(hole_diameter)
)