import cadquery as cq

# Parameters
plate_height = 120.0
plate_thickness = 5.0
plate_width = 10.0
ring_outer_a = 60.0
ring_outer_b = 40.0
ring_wall = 5.0
hole_dia = 6.0
hole_offset = 15.0

# Create the mounting plate
plate = (
    cq.Workplane("XZ")
    .rect(plate_thickness, plate_height)
    .extrude(plate_width)
)

# Create the elliptical ring (washer) profile and extrude
ring = (
    cq.Workplane("XZ")
    .ellipse(ring_outer_a, ring_outer_b)
    .ellipse(ring_outer_a - ring_wall, ring_outer_b - ring_wall)
    .extrude(plate_width)
    .translate((ring_outer_a + plate_thickness/2, 0, 0))
)

# Combine plate and ring
result = plate.union(ring)

# Drill two mounting holes in the plate
z1 = plate_height/2 - hole_offset
z2 = -z1
result = (
    result
    .faces(">Y")
    .workplane()
    .pushPoints([(0, z1), (0, z2)])
    .hole(hole_dia)
)