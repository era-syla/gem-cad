import cadquery as cq

# --- Parametric Dimensions ---
plate_length = 80.0
plate_width = 50.0
plate_thickness = 5.0

hole_diameter = 5.0
countersink_angle = 90.0
countersink_diameter = 8.0  # Slightly larger than hole diameter

# The holes are typically symmetric. Let's place them apart.
hole_spacing = 50.0

# --- Geometry Construction ---

# Create the base plate
result = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_thickness)
)

# Create the points for the holes
# We center them on the face
hole_locations = [
    (-hole_spacing / 2, 0),
    (hole_spacing / 2, 0)
]

# Add countersunk holes
# Select the top face (Z-positive)
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(hole_locations)
    .cskHole(hole_diameter, countersink_diameter, countersink_angle)
)

# If standard counterbored holes were intended instead of countersunk, 
# you would use .cboreHole(...) instead. Based on the visual of a tapered top edge,
# cskHole is the most accurate interpretation.