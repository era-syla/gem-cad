import cadquery as cq
import math

# Geometric Parameters
thickness = 5.0
width_across_flats = 50.0  # Distance from one flat side to the opposite
hole_diameter = 4.0

# Calculate circumscribed diameter needed for the polygon creation
# Relationship: width = diameter * cos(pi/n)
n_sides = 8
angle = math.radians(180 / n_sides)
circum_diameter = width_across_flats / math.cos(angle)

# Generate the CAD model
result = (
    cq.Workplane("XY")
    # Rotate workplane to align flats with X/Y axes (Stop sign orientation)
    .transformed(rotate=(0, 0, 22.5))
    .polygon(nSides=n_sides, diameter=circum_diameter)
    .circle(hole_diameter / 2)
    .extrude(thickness)
)