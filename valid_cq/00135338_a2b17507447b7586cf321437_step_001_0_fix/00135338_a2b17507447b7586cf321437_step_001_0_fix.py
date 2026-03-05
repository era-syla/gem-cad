import cadquery as cq

# Parameters
length = 60
width = 20
plate_thickness = 4
post_diameter = 20
post_height = 40
slot_width = 10
slot_depth = 10
center_hole_diameter = 12

# Create plate
plate = cq.Workplane("XY").box(length, width, plate_thickness)

# Define slot cut positions
slot_rect_centers = [
    ( length/2 - slot_depth/2, 0),
    (-length/2 + slot_depth/2, 0)
]
slot_circle_centers = [
    ( length/2 - slot_depth, 0),
    (-length/2 + slot_depth, 0)
]

# Cut U-shaped slots and center hole
plate = (
    plate
    .faces(">Z").workplane()
    .pushPoints(slot_rect_centers)
    .rect(slot_depth, slot_width)
    .cutThruAll()
    .pushPoints(slot_circle_centers)
    .circle(slot_width/2)
    .cutThruAll()
    .center(0, 0)
    .circle(center_hole_diameter/2)
    .cutThruAll()
)

# Add cylindrical post on bottom
result = (
    plate
    .faces("<Z").workplane()
    .circle(post_diameter/2)
    .extrude(-post_height)
)