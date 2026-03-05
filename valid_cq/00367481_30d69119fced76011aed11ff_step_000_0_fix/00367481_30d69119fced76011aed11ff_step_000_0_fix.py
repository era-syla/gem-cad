import cadquery as cq

# Parameters
rail_radius = 5.0
rail_length = 70.0
frame_width = 30.0
frame_height = 10.0
grip_width = 15.0
grip_thickness = 8.0
grip_height = 60.0
trigger_hole_radius = 7.0

# First rail
rail1 = cq.Workplane("XY") \
    .circle(rail_radius) \
    .extrude(rail_length)

# Second rail
rail2 = cq.Workplane("XY") \
    .transformed(offset=(0, frame_width - 2*rail_radius, 0)) \
    .circle(rail_radius) \
    .extrude(rail_length)

# Combine rails
frame = rail1.union(rail2)

# Top frame plate
top_plate = cq.Workplane("XY") \
    .transformed(offset=(-10, 0, rail_radius)) \
    .rect(rail_length + 20, frame_width) \
    .extrude(frame_height)
frame = frame.union(top_plate)

# Grip block
grip = cq.Workplane("XY") \
    .transformed(offset=(-10 + grip_thickness/2, frame_width/2, frame_height + rail_radius)) \
    .rect(grip_thickness, grip_width) \
    .extrude(grip_height)
frame = frame.union(grip)

# Trigger guard cut
trigger_cut = cq.Workplane("XZ") \
    .transformed(offset=(15, -rail_radius, 5)) \
    .circle(trigger_hole_radius) \
    .extrude(frame_width + 2*rail_radius)
frame = frame.cut(trigger_cut)

# Bottom cavity
cavity = cq.Workplane("XY") \
    .transformed(offset=(30, frame_width/2, 5)) \
    .rect(40, grip_width) \
    .extrude(8)
frame = frame.cut(cavity)

result = frame