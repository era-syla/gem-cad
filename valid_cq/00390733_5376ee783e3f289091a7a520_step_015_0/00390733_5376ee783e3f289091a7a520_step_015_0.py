import cadquery as cq
import math

# Geometric Parameters
length = 50.0               # Total length of the hex standoff
hex_width_across_flats = 12.0  # Distance between parallel faces (wrench size)
hole_diameter = 5.0         # Diameter of the central through-hole
csk_diameter = 7.0          # Diameter of the countersink at the top
csk_angle = 90.0            # Angle of the countersink

# Calculate the circumscribed diameter for the polygon creation
# For a hexagon: Width = sqrt(3)/2 * Diameter -> Diameter = 2 * Width / sqrt(3)
hex_circum_diameter = 2 * hex_width_across_flats / math.sqrt(3)

# Generate the 3D model
result = (
    cq.Workplane("XY")
    # Create the hexagonal base profile
    .polygon(6, hex_circum_diameter)
    # Extrude to create the prism
    .extrude(length)
    # Select the top face
    .faces(">Z")
    .workplane()
    # Create a countersunk hole through the part
    # If depth is not specified, it cuts through the entire solid
    .cskHole(hole_diameter, csk_diameter, csk_angle)
)