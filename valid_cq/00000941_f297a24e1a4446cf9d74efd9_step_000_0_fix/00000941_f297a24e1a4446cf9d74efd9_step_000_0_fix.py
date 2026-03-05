import cadquery as cq

# Parameters
plate_size = 50.0
plate_thickness = 5.0
hole1_pos = (-15.0, 15.0)
hole1_dia = 15.0
hole2_pos = (15.0, 15.0)
hole2_dia = 8.0
rod_dia = 10.0
rod_length = 80.0
disc_dia = 40.0
disc_thickness = 5.0
pocket_dia = 35.0
pocket_depth = 1.0
center_hole_dia = 5.0

# Create plate with two holes
plate = (
    cq.Workplane("XY")
    .rect(plate_size, plate_size)
    .extrude(plate_thickness)
    .faces(">Z")
    .workplane()
    .pushPoints([hole1_pos])
    .circle(hole1_dia/2)
    .cutBlind(-plate_thickness)
    .pushPoints([hole2_pos])
    .circle(hole2_dia/2)
    .cutBlind(-plate_thickness)
)

# Add rod
rod = (
    plate
    .faces(">Z")
    .workplane()
    .circle(rod_dia/2)
    .extrude(rod_length)
)

# Add disc with pocket and center hole
disc = (
    rod
    .faces(">Z")
    .workplane()
    .circle(disc_dia/2)
    .extrude(disc_thickness)
    .faces(">Z")
    .workplane()
    .circle(pocket_dia/2)
    .cutBlind(-pocket_depth)
    .faces(">Z")
    .workplane()
    .circle(center_hole_dia/2)
    .cutThruAll()
)

result = disc