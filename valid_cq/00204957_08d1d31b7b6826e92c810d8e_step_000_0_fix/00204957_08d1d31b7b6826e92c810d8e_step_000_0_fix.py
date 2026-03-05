import cadquery as cq

# Parameters
plate_length = 60
plate_width = 40
plate_thickness = 3

handle_length = 15
handle_width = 10
handle_thickness = plate_thickness

# Hole definitions on the plate
hole_positions = [
    (-plate_length/2 + 8,  plate_width/2 - 8),
    (-plate_length/2 + 20, plate_width/2 - 8),
    (-plate_length/2 + 32, plate_width/2 - 8),
    (-plate_length/2 + 44, plate_width/2 - 8),
]
hole_diameters = [6, 4, 3, 2]

# Build main plate
plate = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# Build handle and union with plate
handle = (
    cq.Workplane("XY")
    .transformed(offset=((plate_length + handle_length) / 2, 0, 0))
    .box(handle_length, handle_width, handle_thickness)
)
result = plate.union(handle)

# Drill holes on top face of plate
for pos, dia in zip(hole_positions, hole_diameters):
    result = (
        result
        .faces(">Z")
        .workplane()
        .pushPoints([pos])
        .hole(dia)
    )

# Cut rectangular slot through handle
slot_margin = 2
slot_length = handle_length - 2 * slot_margin
slot_width = handle_width - 2 * slot_margin
result = (
    result
    .faces(">Z")
    .workplane()
    .transformed(offset=(plate_length/2 + handle_length/2, 0, 0))
    .rect(slot_length, slot_width)
    .cutThruAll()
)