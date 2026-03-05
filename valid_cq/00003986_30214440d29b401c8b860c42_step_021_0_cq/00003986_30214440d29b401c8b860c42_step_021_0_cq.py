import cadquery as cq
import math

# Parameter definitions
num_sides = 8          # Octagonal shape
inner_diameter = 20.0  # Diameter of the finger hole
outer_diameter = 26.0  # Approximate outer diameter (flat-to-flat or corner-to-corner)
thickness = 6.0        # Height/width of the ring band
twist_angle = 15.0     # Angle of twist between top and bottom profiles

# Calculate the radius for the polygon
# outer_diameter here is treated as the circumscribed circle diameter for the polygon
outer_radius = outer_diameter / 2.0

# Create the base polygon wire
# We create a polygon, extrude it with a twist, and then cut the hole.
# To achieve the faceted look, a loft or a twisted extrusion is needed.
# CadQuery's twistExtrude is perfect for this.

result = (
    cq.Workplane("XY")
    .polygon(nSides=num_sides, diameter=outer_diameter)
    .twistExtrude(thickness, twist_angle)
    .faces(">Z").workplane()
    .hole(inner_diameter)
)

# Optional: Adding small chamfers to the inner edges for comfort
# (This is common for rings but might deviate slightly from the pure low-poly look if not careful, 
# strictly looking at the image, the inner edge looks sharp but maybe slightly deburred.
# I will leave it sharp as per the exact geometric interpretation of the image).
# If a comfort fit was needed: result = result.faces("<Z or >Z").edges("%Circle").chamfer(0.5)

# Ensure the result is exported/available
if 'show_object' in globals():
    show_object(result)