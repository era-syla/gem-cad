import cadquery as cq
import math

# Dimensions for the bolt
shaft_diameter = 10.0
shaft_length = 50.0
head_width_across_flats = 17.0
head_height = 7.0

# Calculate the circumscribed diameter of the hexagon based on width across flats
# WAF = R * sqrt(3) => R = WAF / sqrt(3) => Diameter = 2 * WAF / sqrt(3)
head_circum_diameter = 2 * head_width_across_flats / math.sqrt(3)

# Create the geometry
result = (
    cq.Workplane("XY")
    # Create the hexagonal head
    .polygon(6, head_circum_diameter)
    .extrude(head_height)
    # Select the top face of the extruded head
    .faces(">Z")
    .workplane()
    # Create the cylindrical shaft
    .circle(shaft_diameter / 2.0)
    .extrude(shaft_length)
)