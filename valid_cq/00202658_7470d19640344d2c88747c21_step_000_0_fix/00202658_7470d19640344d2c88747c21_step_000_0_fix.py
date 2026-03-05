import cadquery as cq

# Parameters
th = 5
rect_len = 60
body_w = 15
circle_r = 12
finger_len = 10
finger_w = 10
hole1_dia = 6
hole2_dia = 4.5
slot_len = 30
slot_w = 4
slot_offset = 5
hole_spacing = 6

# Build the main rectangular body
result = cq.Workplane("XY").rect(rect_len, body_w).extrude(th)

# Add the circular boss at the right end
result = result.union(
    cq.Workplane("XY")
      .center(rect_len/2, 0)
      .circle(circle_r)
      .extrude(th)
)

# Add the finger tab extending from the boss
result = result.union(
    cq.Workplane("XY")
      .center(rect_len/2 + circle_r + finger_len/2, 0)
      .rect(finger_len, finger_w)
      .extrude(th)
)

# Cut the rectangular slot on the top face of the main body
result = result.faces(">Z") \
    .workplane() \
    .center(-rect_len/2 + slot_offset + slot_len/2, 0) \
    .rect(slot_len, slot_w) \
    .cutThruAll()

# Drill the central hole through the circular boss
result = result.faces(">Z") \
    .workplane() \
    .center(rect_len/2, 0) \
    .hole(hole1_dia)

# Drill two holes through the left end face of the rectangular body
result = result.faces("<X") \
    .workplane(centerOption="CenterOfBoundBox") \
    .pushPoints([(0, hole_spacing/2), (0, -hole_spacing/2)]) \
    .hole(hole2_dia)