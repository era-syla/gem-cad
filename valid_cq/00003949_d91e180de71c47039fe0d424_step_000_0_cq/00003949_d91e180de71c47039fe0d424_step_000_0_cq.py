import cadquery as cq

# --- Parametric Dimensions ---
# Overall dimensions estimation based on visual proportions
body_length = 40.0
body_width = 30.0
body_height = 15.0  # Height of the main lower block

# Back plate (circular flange)
flange_dia = 32.0
flange_thickness = 3.0

# Upper protrusion (the box on top)
top_box_length = 22.0
top_box_width = 16.0
top_box_height = 8.0  # Height added above the main body

# Side arm (the cantilevered part)
arm_length = 15.0  # Length sticking out
arm_width = 4.0
arm_height = 8.0
arm_offset_x = 5.0 # How far back from the front face the cutout starts

# Internal cutouts / connector details
# Main hollow cavity
wall_thickness = 2.0

# Front face cutouts (the two small square-ish ones)
small_port_size = 5.0
small_port_spacing = 8.0

# Side face cutout (large rectangular one)
side_port_width = 12.0
side_port_height = 8.0

# --- Modeling Strategy ---
# 1. Create the back flange (circular disk).
# 2. Create the main rectangular body extruding from the flange.
# 3. Create the top rectangular protrusion.
# 4. Create the side arm structure.
# 5. Perform cuts to hollow out the inside and create the ports.

# --- Construction ---

# 1. Back Flange
flange = (
    cq.Workplane("YZ")
    .circle(flange_dia / 2.0)
    .extrude(flange_thickness)
)

# 2. Main Body Block
# Centering the body relative to the flange might need adjustment. 
# Looking at the image, the body seems roughly centered horizontally but sits lower relative to the circle center.
# Let's align the top of the body slightly below the top of the flange.
body_y_offset = -2.0 # Shift down slightly relative to flange center

main_body = (
    cq.Workplane("YZ")
    .workplane(offset=flange_thickness) # Start after the flange
    .rect(body_width, body_height)
    .extrude(body_length)
    .translate((0, body_y_offset, 0)) # Adjust vertical alignment
)

# 3. Top Box
# Sits on top of the main body
top_box = (
    cq.Workplane("XY")
    .workplane(offset=body_height/2 + body_y_offset) # Start at top of main body
    .center(flange_thickness + top_box_length/2, 0) # Center relative to length
    .rect(top_box_length, top_box_width)
    .extrude(top_box_height)
)

# 4. Side Arm Geometry construction
# The side arm looks like an extension of the side wall that goes forward.
# It seems to be on the left side (negative Y in our current orientation if looking from X+)
# Or, let's stick to standard views:
# Let's assume the flange is at X=0. Main body extends +X.
# Looking from +X towards the origin, the arm is on the left.

arm_y_pos = -body_width/2 + arm_width/2
arm_z_pos = body_height/2 + body_y_offset + arm_height/2 - 2.0 # Roughly aligned with top box base

# The arm seems to originate from the back and extend forward past a cutout.
# Actually, looking closely, there is a slot cut out between the arm and the main top box.
# Let's model the "arm" as a block first, then cut the gap.
arm_block = (
    cq.Workplane("XY")
    .workplane(offset=body_height/2 + body_y_offset)
    .center(flange_thickness + body_length - arm_length/2, -body_width/2 + arm_width/2)
    .rect(arm_length + 10, arm_width) # Make it long enough to merge back
    .extrude(arm_height)
)
# Re-evaluating geometry: It looks like the main body wall extends up on the left side to form the arm.
# Let's simpler add a block for the arm at the front-left corner.
arm_structure = (
    cq.Workplane("XY")
    .workplane(offset=body_height/2 + body_y_offset)
    .center(flange_thickness + body_length + arm_length/2 - 5.0, -body_width/2 + arm_width/2)
    .rect(arm_length, arm_width)
    .extrude(arm_height)
)

# Combined solid before cuts
solid = flange.union(main_body).union(top_box)

# Add the arm extension. The image shows the arm extending beyond the main block face.
arm_extension = (
    cq.Workplane("XY")
    .workplane(offset=body_height/2 + body_y_offset) # Top of main body
    .center(flange_thickness + body_length + 2.5, -body_width/2 + arm_width/2) # Positioned at the corner
    .rect(15, arm_width) # Length of the arm
    .extrude(arm_height) # Height of the arm
)

solid = solid.union(arm_extension)

# Fill the gap behind the arm extension to connect it to the flange/body
arm_connector = (
     cq.Workplane("XY")
    .workplane(offset=body_height/2 + body_y_offset)
    .center(flange_thickness + body_length/2, -body_width/2 + arm_width/2)
    .rect(body_length, arm_width)
    .extrude(arm_height) 
)
# We will cut the slot later
solid = solid.union(arm_connector)


# --- Cuts ---

# 1. Main Hollow Shelling
# It's a shell, but we need specific wall thicknesses.
# Let's cut a large pocket from the bottom or front.
# The image implies the interior is hollow and accessible from the front/ports.

# Let's create a core to remove material from the main body
core_width = body_width - 2*wall_thickness
core_height = body_height - 2*wall_thickness
core = (
    cq.Workplane("YZ")
    .workplane(offset=flange_thickness - 1.0) # Start slightly inside flange
    .rect(core_width, core_height)
    .extrude(body_length + 20) # Cut all the way through front
    .translate((0, body_y_offset, 0))
)
solid = solid.cut(core)


# 2. Side Ports (Right side of image, +Y in our coords)
# There is a large rectangular cutout on the side.
side_cut = (
    cq.Workplane("XZ")
    .workplane(offset=body_width/2 + 5.0) # Start outside
    .center(flange_thickness + body_length/2 + 5, body_y_offset)
    .rect(14, 8)
    .extrude(-10) # Cut inward
)
solid = solid.cut(side_cut)

# 3. Another side port near the front
side_cut_front = (
    cq.Workplane("XZ")
    .workplane(offset=body_width/2 + 5.0)
    .center(flange_thickness + body_length - 8, body_y_offset)
    .rect(10, 8)
    .extrude(-10)
)
solid = solid.cut(side_cut_front)


# 4. Front Ports (Small square ones on the bottom front face)
# Based on the image, there are two small square ports on the lower left face
front_ports = (
    cq.Workplane("YZ")
    .workplane(offset=flange_thickness + body_length) # On the front face
    .center(-body_width/4, body_y_offset - body_height/4) # Approximate position
    .rect(small_port_size, small_port_size)
    .extrude(-wall_thickness * 2) # Cut inward
)
# Make a second one next to it
front_port_2 = (
    cq.Workplane("YZ")
    .workplane(offset=flange_thickness + body_length)
    .center(-body_width/4 + small_port_spacing, body_y_offset - body_height/4)
    .rect(small_port_size, small_port_size)
    .extrude(-wall_thickness * 2)
)
solid = solid.cut(front_ports).cut(front_port_2)

# 5. Slot Cut behind the arm
# There is a distinct gap between the "arm" (left side wall extension) and the central "top box".
slot_cut = (
    cq.Workplane("XY")
    .workplane(offset=body_height/2 + body_y_offset + 10) # Start above
    .center(flange_thickness + body_length/2 + 5, -body_width/2 + arm_width + 1.5) # Position between arm and center
    .rect(body_length, 3.0) # Slot width
    .extrude(-20) # Cut down
)
solid = solid.cut(slot_cut)

# 6. Refine the arm length/shape
# The arm sticks out quite a bit. Let's ensure the cut creates the cantilever effect.
# We need to cut the material *under* the cantilever arm extension at the front.
# The previous shelling might have done this, but let's ensure the arm floats.
# The arm is defined by `arm_extension`. It sits on top of Z plane.
# The `core` cut removed the inside of the main body, but not necessarily under the protruding arm if the arm is longer than the body.

# Actually, visually, the arm is an extension of the SIDE WALL.
# The slot cut separated it from the top block.

# 7. Chamfers and Fillets
# The back flange top edge is slightly rounded or chamfered? Hard to see.
# The top box front corners look sharp.
# The flange has a flat bottom cut or is intersected by the box.
# Let's fillet the top edge of the flange for aesthetics as shown in render (smooth).
try:
    solid = solid.edges(cq.selectors.NearestToPointSelector((0, 0, flange_dia/2))).fillet(1.0)
except:
    pass # If selection fails, skip

# Correcting the flange flat bottom.
# In the image, the circular flange doesn't go below the rectangular body much.
# Let's cut the bottom of the flange flat to match the body bottom.
bottom_cut = (
    cq.Workplane("XY")
    .workplane(offset=-20)
    .rect(100, 100)
    .extrude(20 + (body_y_offset - body_height/2))
)
solid = solid.cut(bottom_cut)

result = solid