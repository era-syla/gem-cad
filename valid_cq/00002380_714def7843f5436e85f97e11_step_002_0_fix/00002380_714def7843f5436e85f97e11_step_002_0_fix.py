import cadquery as cq

# Parameters
plate_thickness = 5
frame_outer_width = 80
frame_outer_height = 40
frame_depth = plate_thickness
frame_inner_width = frame_outer_width - 2 * frame_depth
frame_inner_height = frame_outer_height - 2 * frame_depth
side_plate_length = 60
pivot_dia = 8
ring_outer_dia = 30
ring_inner_dia = 24
ring_thickness = 5

# Rectangular frame
frame = (
    cq.Workplane("XY")
    .rect(frame_outer_width, frame_outer_height)
    .extrude(frame_depth)
    .faces(">Z")
    .workplane()
    .rect(frame_inner_width, frame_inner_height)
    .cutBlind(-frame_depth)
)

# Side plate profile
plate_profile = [
    (frame_outer_width/2,  frame_outer_height/2),
    (frame_outer_width/2 + side_plate_length,  0),
    (frame_outer_width/2, -frame_outer_height/2)
]

# Create one side plate and mirror for the other
plate = (
    cq.Workplane("XY")
    .polyline(plate_profile)
    .close()
    .extrude(plate_thickness)
)
plates = plate.union(plate.mirror("YZ"))

# Pivot pin (cylinder through side plates)
pivot_length = frame_outer_width/2 + side_plate_length + 10
pivot = (
    cq.Workplane("YZ")
    .circle(pivot_dia/2)
    .extrude(pivot_length)
    .translate((frame_outer_width/2 + side_plate_length/2, 0, plate_thickness/2))
)

# Clamp ring
ring = (
    cq.Workplane("YZ")
    .workplane(offset=frame_outer_width/2 + side_plate_length - ring_thickness/2)
    .circle(ring_outer_dia/2)
    .circle(ring_inner_dia/2)
    .extrude(ring_thickness)
)

# Assemble result
result = frame.union(plates).union(pivot).union(ring)