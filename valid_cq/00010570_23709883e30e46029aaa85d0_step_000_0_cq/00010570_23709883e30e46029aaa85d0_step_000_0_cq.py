import cadquery as cq

# Parameters
base_diameter = 10.0
base_length = 30.0
hex_flat_to_flat = 6.0  # Common size for a hex shaft relative to the base
hex_length = 25.0
hole_diameter = 2.0
hole_offset = 3.0       # Distance from the bottom of the base

# Create the Base Cylinder
# We start at the origin (0,0,0) and extrude upwards
base = cq.Workplane("XY").circle(base_diameter / 2.0).extrude(base_length)

# Create the Hexagonal Shaft
# We select the top face of the cylinder to start the hex extrusion
# The polygon method uses the circumscribed radius. 
# For a hex, circumscribed radius = flat_to_flat / sqrt(3) 
# Or simpler: polygon(6, diameter) in CadQuery usually defines the outer diameter (circumscribed circle) 
# To get specific flat-to-flat (S), circumscribed diameter (D) is D = S / cos(30) = S / (sqrt(3)/2)
import math
hex_circumscribed_diameter = hex_flat_to_flat / (math.sqrt(3) / 2)

shaft = (
    base.faces(">Z")
    .workplane()
    .polygon(nSides=6, diameter=hex_circumscribed_diameter)
    .extrude(hex_length)
)

# Create the Through Hole in the Base
# We look at the base cylinder, select a plane perpendicular to the axis (like XZ or YZ)
# and offset it to drill through.
result = (
    shaft.faces("<Z") # Go back to bottom face
    .workplane(offset=hole_offset) # Move plane up to hole location
    .transformed(rotate=(90, 0, 0)) # Rotate to drill perpendicular to Z axis
    .hole(hole_diameter)
)

# Alternatively, a more robust way to place the hole relative to the origin:
# result = shaft.faces("<Z").workplane().transformed(offset=(0, 0, hole_offset), rotate=(90, 0, 0)).hole(hole_diameter)

# Final result variable required
result = result