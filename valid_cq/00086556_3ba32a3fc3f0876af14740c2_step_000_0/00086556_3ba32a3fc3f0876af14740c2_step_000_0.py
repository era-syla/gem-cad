import cadquery as cq

# --- Parametric Dimensions ---
width = 30.0           # Overall width (Y-axis)
cyl_radius = 12.5      # Radius of the cylindrical base
arm_length = 60.0      # Length of the rectangular arm from origin
arm_height = 18.0      # Height of the rectangular arm
slot_width = 12.0      # Width of the fork slot
slot_offset = 20.0     # Distance from cylinder center to slot end
hole_diameter = 3.0    # Diameter of the locking pin hole

# --- Modeling ---

# 1. Create the cylindrical base
# Oriented with axis along Y, centered at origin
base_cyl = (
    cq.Workplane("XZ")
    .circle(cyl_radius)
    .extrude(width/2, both=True)
)

# 2. Create the rectangular arm
# Extends along -X, top flush with cylinder top
arm_box = (
    cq.Workplane("XY")
    .box(arm_length, width, arm_height)
    # Position: Centered on Y, Top at Z=R, Right face at X=0
    .translate((-arm_length/2, 0, cyl_radius - arm_height/2))
)

# Union the base and arm
body = base_cyl.union(arm_box)

# 3. Cut the Slot
# Define cut geometry on the top face
slot_center_x = -slot_offset

# 3a. Cut the rounded end of the slot
body = body.cut(
    cq.Workplane("XY")
    .workplane(offset=cyl_radius)
    .moveTo(slot_center_x, 0)
    .circle(slot_width/2)
    .extrude(-arm_height * 2)  # Cut through downwards
)

# 3b. Cut the straight rectangular channel of the slot
# Center of this cut rect needs to be positioned correctly
cut_rect_len = arm_length # Make it long enough to clear the tip
body = body.cut(
    cq.Workplane("XY")
    .workplane(offset=cyl_radius)
    .moveTo(slot_center_x - cut_rect_len/2, 0)
    .rect(cut_rect_len, slot_width)
    .extrude(-arm_height * 2)
)

# 4. Create the side hole
# Positioned on the side face, going through both prongs
hole_z = cyl_radius - (arm_height / 2) # Centered vertically on the arm

result = (
    body
    .faces(">Y") # Select the positive Y face
    .workplane()
    .moveTo(slot_center_x, hole_z)
    .hole(hole_diameter)
)

# Export or display
# show_object(result)