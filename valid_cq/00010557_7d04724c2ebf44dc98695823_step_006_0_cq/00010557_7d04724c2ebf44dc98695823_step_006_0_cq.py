import cadquery as cq

# Parametric dimensions
main_disk_radius = 25.0
main_disk_thickness = 10.0
center_shaft_radius = 2.5
center_shaft_length = 50.0  # Length sticking out from the back
offset_pin_radius = 2.5
offset_pin_length = 15.0  # Length sticking out from the front
offset_pin_distance = 15.0 # Distance from center

# Create the main disk
# We'll center the disk on the origin for simplicity
main_disk = cq.Workplane("XY").circle(main_disk_radius).extrude(main_disk_thickness)

# Create the long center shaft
# It seems to come out from the "back" of the disk (negative Z direction relative to front face)
# We can start from the back face and extrude away
center_shaft = (
    main_disk.faces("<Z")
    .workplane()
    .circle(center_shaft_radius)
    .extrude(center_shaft_length)
)

# Create the small offset pin
# It comes out from the "front" of the disk (positive Z direction)
# It is offset from the center
result = (
    center_shaft.faces(">Z")
    .workplane()
    .center(offset_pin_distance, 0)
    .circle(offset_pin_radius)
    .extrude(offset_pin_length)
)