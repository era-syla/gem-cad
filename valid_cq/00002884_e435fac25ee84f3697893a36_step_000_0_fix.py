import cadquery as cq

# Base block
base = cq.Workplane("XY").box(80, 60, 15)

# Servo horn / arm - elongated shape with rounded ends
arm_length = 70
arm_width = 12
arm_thickness = 4

# Create the servo horn arm as an elongated rounded rectangle
arm = (
    cq.Workplane("XY")
    .workplane(offset=20)
    .center(-10, 40)
)

# Build the arm body - capsule shape (rounded ends)
arm_body = (
    cq.Workplane("XY")
    .workplane(offset=20)
)

# Create arm as a hull-like shape using union of circles and rectangle
# Left end circle
c1 = cq.Workplane("XY").workplane(offset=20).center(-10 + (-arm_length/2 + arm_width/2), 40).circle(arm_width/2).extrude(arm_thickness)
# Right end circle
c2 = cq.Workplane("XY").workplane(offset=20).center(-10 + (arm_length/2 - arm_width/2), 40).circle(arm_width/2).extrude(arm_thickness)
# Middle rectangle
rect_part = (
    cq.Workplane("XY")
    .workplane(offset=20)
    .center(-10, 40)
    .rect(arm_length - arm_width, arm_width)
    .extrude(arm_thickness)
)

arm_solid = c1.union(c2).union(rect_part)

# Center hub - raised circular boss
hub = (
    cq.Workplane("XY")
    .workplane(offset=20 + arm_thickness)
    .center(-10, 40)
    .circle(arm_width/2 - 1)
    .extrude(2)
)

arm_solid = arm_solid.union(hub)

# Add holes along the arm
# Center hole (for mounting screw)
arm_solid = (
    arm_solid
    .faces(">Z")
    .workplane()
    .center(-10 - (-10), 40 - 40)  # relative to face center... let's use absolute approach
)

# Cut holes using absolute positioning
hole_positions_x = [-10 + i * 8 for i in range(-3, 5)]

for hx in hole_positions_x:
    arm_solid = (
        cq.Workplane("XY")
        .workplane(offset=20)
        .center(hx, 40)
        .circle(1.5)
        .extrude(arm_thickness + 2)
        .val()
    )
    # We'll do the cuts differently

# Rebuild arm with holes cut properly
arm_solid = c1.union(c2).union(rect_part).union(hub)

# Cut small holes along the arm
for i, hx in enumerate(hole_positions_x):
    cut_cyl = (
        cq.Workplane("XY")
        .workplane(offset=19)
        .center(hx, 40)
        .circle(1.5)
        .extrude(arm_thickness + 4)
    )
    arm_solid = arm_solid.cut(cut_cyl)

# Cut center larger hole through hub
center_hole = (
    cq.Workplane("XY")
    .workplane(offset=19)
    .center(-10, 40)
    .circle(2.5)
    .extrude(arm_thickness + 6)
)
arm_solid = arm_solid.cut(center_hole)

# Rotate the arm slightly to match the image (arm is angled)
arm_solid = arm_solid.rotate((0, 0, 0), (0, 0, 1), 30)

# Combine base and arm
result = base.union(arm_solid)