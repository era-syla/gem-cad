import cadquery as cq
import math

# --- Parameters ---
# Main body dimensions
body_diameter = 10.0
body_length = 50.0

# Front hole dimensions
hole_diameter = 3.5
hole_depth = 8.0

# Rear hex fitting dimensions
hex_across_flats = 9.0
hex_thickness = 3.0

# Wire dimensions
wire_diameter = 1.2
wire_length = 15.0
wire_angle = 10.0  # Slight angle to match the image perspective

# --- Geometry Construction ---

# 1. Create the main cylindrical body
# Aligning along the X-axis
result = cq.Workplane("YZ").circle(body_diameter / 2.0).extrude(body_length)

# 2. Create the hole in the front face (Face at +X)
result = result.faces(">X").workplane().hole(hole_diameter, hole_depth)

# 3. Add a chamfer to the outer edge of the front face
# Using NearestToPointSelector to specifically target the outer circumference edge
result = result.edges(cq.NearestToPointSelector((body_length, body_diameter/2.0, 0))).chamfer(0.5)

# 4. Create the hexagonal fitting at the rear (Face at -X)
# Calculate the circumdiameter (diameter of circle passing through vertices)
# circum_diameter = across_flats / cos(30 degrees)
hex_circum_diameter = hex_across_flats / math.cos(math.radians(30))

# Extrude the hexagon from the rear face
# Note: The workplane on the <X face has a normal pointing in -X. 
# Positive extrusion adds material in the -X direction.
result = (
    result.faces("<X")
    .workplane()
    .polygon(6, hex_circum_diameter)
    .extrude(hex_thickness)
)

# 5. Create the wire/lead extending from the rear
# We tilt the workplane slightly to mimic the angled appearance in the reference image
result = (
    result.faces("<X")
    .workplane()
    .transformed(rotate=(0, -wire_angle, 0)) # Tilt around Y-axis to point wire slightly "up" in Z
    .circle(wire_diameter / 2.0)
    .extrude(wire_length)
)