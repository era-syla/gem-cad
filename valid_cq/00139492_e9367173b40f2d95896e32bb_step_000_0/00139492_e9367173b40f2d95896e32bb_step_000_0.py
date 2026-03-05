import cadquery as cq

# -- Parametric Dimensions --
length = 100.0        # Total length of the arm
width = 24.0          # Width of the arm (and diameter of the rounded ends)
thickness = 5.0       # Thickness of the main plate
hole_diameter = 12.0  # Diameter of the through-hole on the left
boss_diameter = 10.0  # Diameter of the pin/boss on the right
boss_height = 6.0     # Height of the pin/boss protruding from the face

# Calculate offset from center (0,0) to the center of the rounded ends
# slot2D creates a shape centered at origin with total length and width
end_center_offset = (length - width) / 2.0

# -- Model Generation --

# 1. Create the main body (stadium/slot shape)
result = (
    cq.Workplane("XY")
    .slot2D(length, width)
    .extrude(thickness)
)

# 2. Cut the through-hole on the left end (-X side)
# We select the top face, move to the center of the left arc, and cut
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(-end_center_offset, 0)])
    .circle(hole_diameter / 2.0)
    .cutThruAll()
)

# 3. Add the boss/pin on the right end (+X side)
# We select the bottom face (<Z) to extrude the boss downwards 
# (or upwards relative to the inverted plane, creating a protrusion on the back)
result = (
    result.faces("<Z")
    .workplane()
    .pushPoints([(end_center_offset, 0)])
    .circle(boss_diameter / 2.0)
    .extrude(boss_height)
)