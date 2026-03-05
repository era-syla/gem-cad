import cadquery as cq

# -- Parameters --
thickness = 10.0
vert_width = 30.0
vert_height = 75.0      # Distance from hole center to top edge
arm_height = 25.0       # Vertical height of the top horizontal arm section
arm_reach = 40.0        # X-distance from origin to the start of the arm's end arc
hole_dia = 10.0         # Diameter of bottom hole
slot_length = 32.0      # Total length of the slot
slot_width = 8.0        # Width of the slot
fillet_tl = 10.0        # Radius of top-left corner fillet
fillet_inner = 10.0     # Radius of inner neck fillet

# -- Derived Coordinates --
x_left = -vert_width / 2.0
x_right = vert_width / 2.0
y_top = vert_height
y_arm_bot = vert_height - arm_height
r_bottom = vert_width / 2.0
r_arm = arm_height / 2.0

# -- Model Construction --

# 1. Generate the base profile sketch and extrude
result = (
    cq.Workplane("XY")
    .moveTo(x_left, 0)
    .lineTo(x_left, y_top)                    # Left vertical straight edge
    .lineTo(arm_reach, y_top)                 # Top horizontal straight edge
    .threePointArc(                           # Right-side semi-circle end
        (arm_reach + r_arm, y_top - r_arm),   # Arc midpoint
        (arm_reach, y_arm_bot)                # Arc endpoint
    )
    .lineTo(x_right, y_arm_bot)               # Bottom edge of the arm
    .lineTo(x_right, 0)                       # Right vertical straight edge
    .threePointArc(                           # Bottom semi-circle
        (0, -r_bottom),                       # Arc midpoint
        (x_left, 0)                           # Arc endpoint
    )
    .close()
    .extrude(thickness)
)

# 2. Apply fillets
# Top-Left Corner: Select vertical edge at (x_left, y_top)
result = result.edges(cq.NearestToPointSelector((x_left, y_top, thickness/2))).fillet(fillet_tl)

# Inner Connection Corner: Select vertical edge at (x_right, y_arm_bot)
result = result.edges(cq.NearestToPointSelector((x_right, y_arm_bot, thickness/2))).fillet(fillet_inner)

# 3. Create Bottom Hole
result = (
    result.faces(">Z")
    .workplane()
    .moveTo(0, 0)
    .hole(hole_dia)
)

# 4. Create Top Slot
# Calculate position to match visual proportion
slot_y = y_top - r_arm
slot_center_x = 28.0  # Centered based on arm proportions

result = (
    result.faces(">Z")
    .workplane()
    .moveTo(slot_center_x, slot_y)
    .slot2D(slot_length, slot_width)
    .cutThruAll()
)