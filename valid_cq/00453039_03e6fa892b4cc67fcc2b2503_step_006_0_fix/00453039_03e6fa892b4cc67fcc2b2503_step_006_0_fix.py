import cadquery as cq

# Parameters
plate_length = 80
plate_height = 40
plate_thickness = 5

standoff_outer_radius = 6
standoff_height = 8
standoff_inner_radius = 3

cutout_width = 12
cutout_height = 8

screw_hole_diameter = 4

# Base plate: rectangle in X (length) and Z (height), extruded in Y (thickness)
result = cq.Workplane("XZ").rect(plate_length, plate_height).extrude(plate_thickness)

# Standoffs on front face (+Y)
standoff_positions = [(-30, -plate_height/2), (0, -plate_height/2), (30, -plate_height/2)]
for x, z in standoff_positions:
    # Outer cylinder
    result = result.union(
        cq.Workplane("XZ")
        .workplane(offset=plate_thickness)
        .center(x, z)
        .circle(standoff_outer_radius)
        .extrude(standoff_height)
    )

# Inner pocket in each standoff
for x, z in standoff_positions:
    result = result.faces(">Y").workplane().center(x, z).hole(
        standoff_inner_radius * 2, standoff_height
    )

# Rectangular cutouts through the plate
cutout_positions = [(-20, 5), (20, 5)]
result = result.faces(">Y").workplane().pushPoints(cutout_positions).rect(
    cutout_width, cutout_height
).cutThruAll()

# Screw holes around the cutouts
screw_positions = [(-25, 12), (25, 12), (-25, -12), (25, -12)]
result = result.faces(">Y").workplane().pushPoints(screw_positions).hole(
    screw_hole_diameter, plate_thickness + 1
)