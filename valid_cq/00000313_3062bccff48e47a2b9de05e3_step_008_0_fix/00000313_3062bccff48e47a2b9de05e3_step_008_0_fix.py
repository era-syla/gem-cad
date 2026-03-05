import cadquery as cq

# Parameters
outer_r = 18
inner_r = 14
arm_length = 35
center_r = 22
slot_w = 4
slot_h = 8
slot_depth = 3

# Create the central sphere/hub
result = cq.Workplane("XY").sphere(center_r)

# Function to create a hollow cylinder arm
def make_arm(direction):
    # Outer cylinder
    arm = cq.Workplane("XY")
    
    if direction == "X+":
        arm = cq.Workplane("YZ").circle(outer_r).extrude(arm_length)
        arm = arm.translate((0, 0, 0))
        # Actually build along X
        arm = cq.Workplane("YZ").workplane(offset=0).circle(outer_r).extrude(arm_length)
    
    return arm

# Build arms in all 6 directions using unions
# X direction arms
arm_x_pos = cq.Workplane("YZ").circle(outer_r).extrude(arm_length)
arm_x_neg = cq.Workplane("YZ").workplane(offset=-arm_length).circle(outer_r).extrude(-arm_length)

# Y direction arms  
arm_y_pos = cq.Workplane("XZ").circle(outer_r).extrude(arm_length)
arm_y_neg = cq.Workplane("XZ").workplane(offset=-arm_length).circle(outer_r).extrude(-arm_length)

# Z direction arms
arm_z_pos = cq.Workplane("XY").circle(outer_r).extrude(arm_length)
arm_z_neg = cq.Workplane("XY").workplane(offset=-arm_length).circle(outer_r).extrude(-arm_length)

# Central hub
hub = cq.Workplane("XY").sphere(center_r)

# Union all arms with hub
result = hub.union(arm_x_pos).union(arm_x_neg).union(arm_y_pos).union(arm_y_neg).union(arm_z_pos).union(arm_z_neg)

# Now hollow out each arm with inner cylinders
hole_x = cq.Workplane("YZ").circle(inner_r).extrude(arm_length + 5)
hole_x_neg = cq.Workplane("YZ").workplane(offset=-(arm_length+5)).circle(inner_r).extrude(arm_length + 5)
hole_y = cq.Workplane("XZ").circle(inner_r).extrude(arm_length + 5)
hole_y_neg = cq.Workplane("XZ").workplane(offset=-(arm_length+5)).circle(inner_r).extrude(arm_length + 5)
hole_z = cq.Workplane("XY").circle(inner_r).extrude(arm_length + 5)
hole_z_neg = cq.Workplane("XY").workplane(offset=-(arm_length+5)).circle(inner_r).extrude(arm_length + 5)

result = result.cut(hole_x).cut(hole_x_neg).cut(hole_y).cut(hole_y_neg).cut(hole_z).cut(hole_z_neg)

# Add slots on each arm end - keyhole style slots
# Slots on X+ arm end face
def make_slot_x_pos(angle_deg):
    import math
    angle = math.radians(angle_deg)
    y = (outer_r - slot_depth/2) * math.cos(angle)
    z = (outer_r - slot_depth/2) * math.sin(angle)
    slot = (cq.Workplane("YZ")
            .workplane(offset=arm_length - slot_h/2)
            .center(y, z)
            .rect(slot_w, slot_h)
            .extrude(slot_depth + 2))
    return slot

for angle in [45, 135, 225, 315]:
    s = make_slot_x_pos(angle)
    result = result.cut(s)

def make_slot_x_neg(angle_deg):
    import math
    angle = math.radians(angle_deg)
    y = (outer_r - slot_depth/2) * math.cos(angle)
    z = (outer_r - slot_depth/2) * math.sin(angle)
    slot = (cq.Workplane("YZ")
            .workplane(offset=-(arm_length - slot_h/2 + slot_depth + 2))
            .center(y, z)
            .rect(slot_w, slot_h)
            .extrude(slot_depth + 2))
    return slot

for angle in [45, 135, 225, 315]:
    s = make_slot_x_neg(angle)
    result = result.cut(s)

def make_slot_z_pos(angle_deg):
    import math
    angle = math.radians(angle_deg)
    x = (outer_r - slot_depth/2) * math.cos(angle)
    y = (outer_r - slot_depth/2) * math.sin(angle)
    slot = (cq.Workplane("XY")
            .workplane(offset=arm_length - slot_h/2)
            .center(x, y)
            .rect(slot_w, slot_h)
            .extrude(slot_depth + 2))
    return slot

for angle in [45, 135, 225, 315]:
    s = make_slot_z_pos(angle)
    result = result.cut(s)