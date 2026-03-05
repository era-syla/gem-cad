import cadquery as cq

# --- Parameters ---
# Head dimensions
head_width = 32.0
head_radius = head_width / 2.0
head_flat_height = 20.0  # Height of the straight vertical section below hole center
head_thickness = 10.0
hole_diameter = 18.0

# Arm dimensions
arm_length = 85.0
arm_height = 6.0
arm_thickness = 4.0
arm_tip_radius = arm_height / 2.0

# Small hole dimensions
small_hole_diameter = 2.0
small_hole_dist_from_base = 8.0

# --- Modeling ---

# 1. Create the Head
# The head shape is defined by a profile on the XY plane: a semi-circle on top and a rectangle below.
# The origin (0,0,0) is placed at the center of the large hole.
head = (
    cq.Workplane("XY")
    .moveTo(head_radius, 0)
    .threePointArc((0, head_radius), (-head_radius, 0))  # Top semi-circle
    .lineTo(-head_radius, -head_flat_height)             # Left vertical side
    .lineTo(head_radius, -head_flat_height)              # Bottom horizontal side
    .lineTo(head_radius, 0)                              # Right vertical side
    .close()
    .circle(hole_diameter / 2.0)                         # Cut the main large hole
    .extrude(head_thickness)
)

# 2. Create the Arm
# The arm is attached to the left side of the head, aligned with the bottom edge.
# It is thinner than the head, so we offset the workplane in Z to center it.
arm_z_offset = (head_thickness - arm_thickness) / 2.0
arm_y_bottom = -head_flat_height

arm = (
    cq.Workplane("XY")
    .workplane(offset=arm_z_offset)
    .moveTo(-head_radius, arm_y_bottom)                        # Start at bottom-left corner of head
    .lineTo(-head_radius - arm_length, arm_y_bottom)           # Draw bottom edge outwards
    .lineTo(-head_radius - arm_length, arm_y_bottom + arm_height) # Draw vertical tip edge
    .lineTo(-head_radius, arm_y_bottom + arm_height)           # Draw top edge back to head
    .close()
    .extrude(arm_thickness)
)

# 3. Refine the Arm
# Apply a full fillet to the tip of the arm.
# We select the vertical edge at the far end (minimum X).
tip_edge_selector = cq.selectors.NearestToPointSelector((-head_radius - arm_length, arm_y_bottom + arm_height/2.0))
arm = arm.edges(tip_edge_selector).fillet(arm_tip_radius - 0.01)

# Create the small hole through the arm near the connection point.
small_hole_x = -head_radius - small_hole_dist_from_base
small_hole_y = arm_y_bottom + (arm_height / 2.0)

arm = (
    arm.faces(">Z")
    .workplane()
    .pushPoints([(small_hole_x, small_hole_y)])
    .hole(small_hole_diameter)
)

# 4. Combine Head and Arm into a single solid
result = head.union(arm)