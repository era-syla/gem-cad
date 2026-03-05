import cadquery as cq

# Parameters
plate_length = 100.0
plate_width = 12.0
plate_thickness = 5.0
web_height = 20.0
arm_thickness = 5.0
arm_gap = 12.0
hole_dia = 4.0
indent_width = 40.0
indent_depth = 3.0
tail_hole_offset = 10.0

# Main plate
plate = cq.Workplane("XY").rect(plate_length, plate_width).extrude(plate_thickness)

# Bottom arc indentation
plate = (
    plate
    .faces("<Z")
    .workplane()
    .moveTo(-indent_width/2, 0)
    .threePointArc((0, indent_depth), (indent_width/2, 0))
    .close()
    .cutBlind(-indent_depth)
)

# Compute prong centers (plate is centered at origin)
right_prong_center = plate_length/2 - arm_thickness/2
left_prong_inner = plate_length/2 - arm_thickness
left_prong_center = left_prong_inner - arm_gap - arm_thickness/2
prong_centers = [(left_prong_center, 0), (right_prong_center, 0)]

# Add vertical prongs on top of plate
plate = (
    plate
    .faces(">Z")
    .workplane()
    .pushPoints(prong_centers)
    .rect(arm_thickness, plate_width)
    .extrude(web_height)
)

# Hole centers (X,Z) for prongs and plate
hole_centers = [
    (left_prong_center, plate_thickness + web_height/2),
    (right_prong_center, plate_thickness + web_height/2),
    (0.0, plate_thickness/2),
    (-plate_length/2 + tail_hole_offset, plate_thickness/2),
]

# Create through-holes by cutting cylinders along Y
holes = (
    cq.Workplane("XZ", origin=(0, -plate_width/2, 0))
    .pushPoints(hole_centers)
    .circle(hole_dia/2)
    .extrude(plate_width)
)

result = plate.cut(holes)