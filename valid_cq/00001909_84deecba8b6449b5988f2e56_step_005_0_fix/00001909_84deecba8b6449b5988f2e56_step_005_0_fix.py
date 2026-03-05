import cadquery as cq

# Parameters
thickness = 3.0
arm_width = 12.0
arm_length = 50.0
hole_dia = 5.0
slot_length = 30.0
slot_width = 6.0
slot_gap = 14.0

# Create horizontal and vertical bars
arm_h = cq.Workplane("XY").rect(2*arm_length, arm_width).extrude(thickness)
arm_v = cq.Workplane("XY").rect(arm_width, 2*arm_length).extrude(thickness)

# Create circular end caps
cap1 = cq.Workplane("XY").circle(arm_width/2).translate(( arm_length,  0)).extrude(thickness)
cap2 = cq.Workplane("XY").circle(arm_width/2).translate((-arm_length,  0)).extrude(thickness)
cap3 = cq.Workplane("XY").circle(arm_width/2).translate(( 0,  arm_length)).extrude(thickness)
cap4 = cq.Workplane("XY").circle(arm_width/2).translate(( 0, -arm_length)).extrude(thickness)

# Union all solid pieces into one body
result = arm_h.union(arm_v).union(cap1).union(cap2).union(cap3).union(cap4)

# Cut out mounting holes at ends
hole_positions = [
    ( arm_length,  0),
    (-arm_length,  0),
    ( 0,  arm_length),
    ( 0, -arm_length),
]
result = result.faces(">Z").workplane().pushPoints(hole_positions).circle(hole_dia/2).cutThruAll()

# Cut two rectangular slots in center
slot_positions = [
    (0,  slot_gap/2),
    (0, -slot_gap/2),
]
result = result.faces(">Z").workplane().pushPoints(slot_positions).rect(slot_length, slot_width).cutThruAll()