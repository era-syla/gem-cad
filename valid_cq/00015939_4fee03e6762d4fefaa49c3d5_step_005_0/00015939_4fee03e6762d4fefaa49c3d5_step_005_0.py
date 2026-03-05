import cadquery as cq

# -- Parametric Dimensions --
hex_outer_diameter = 100.0  # Circumscribed diameter of the hexagon (vertex-to-vertex)
base_thickness = 3.0        # Thickness of the hexagonal base plate
disk_diameter = 80.0        # Diameter of the central circular platform
disk_height = 2.0           # Height/thickness of the central platform
hole_diameter = 4.0         # Diameter of the mounting holes
hole_pattern_radius = 45.0  # Distance from center to the hole centers

# -- Modeling Steps --

# 1. Create the hexagonal base plate
# polygon(6, dia) creates a hexagon inscribed in a circle of the given diameter.
# Default orientation places vertices at 0, 60, 120... degrees.
result = cq.Workplane("XY").polygon(6, hex_outer_diameter).extrude(base_thickness)

# 2. Add the central circular disk
# Select the top face of the hexagon, draw the circle, and extrude upwards.
result = (
    result.faces(">Z")
    .workplane()
    .circle(disk_diameter / 2.0)
    .extrude(disk_height)
)

# 3. Cut the mounting holes
# Select the bottom face to define the hole locations.
# Create a polar array of 6 points aligned with the hexagon vertices (starting at angle 0).
# .hole() cuts a through-hole (implied through-all if no depth specified, or typically deep enough).
result = (
    result.faces("<Z")
    .workplane()
    .polarArray(radius=hole_pattern_radius, startAngle=0, angle=360, count=6)
    .hole(hole_diameter)
)