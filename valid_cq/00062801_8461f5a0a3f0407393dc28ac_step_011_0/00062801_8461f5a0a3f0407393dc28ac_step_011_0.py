import cadquery as cq

# Parametric dimensions based on the visual estimation
plate_length = 90.0
plate_width = 30.0
plate_thickness = 3.0
hole_diameter = 10.0

# Calculate spacing: place outer holes at the centers of the rounded ends
# The straight section length is (plate_length - plate_width)
# Distance from center to radius center is half of that
center_offset = (plate_length - plate_width) / 2.0

# Define hole locations: Center, Left, Right
hole_locations = [(0, 0), (-center_offset, 0), (center_offset, 0)]

# Generate geometry
result = (
    cq.Workplane("XY")
    .slot2D(plate_length, plate_width)
    .extrude(plate_thickness)
    .faces(">Z")
    .workplane()
    .pushPoints(hole_locations)
    .hole(hole_diameter)
)