import cadquery as cq

# --- Parameters ---
length = 120.0       # Total length of the case
width = 65.0         # Total width of the case
height = 12.0        # Total height of the walls
wall_thickness = 1.5 # Thickness of the outer walls and bottom
fillet_radius = 8.0  # Corner radius of the case

# Cutout dimensions (estimated from visual proportion)
camera_cutout_size = 12.0
camera_pos_x = -length/2 + 25.0
camera_pos_y = width/2 - 15.0

flash_dia = 5.0
flash_pos_x = -length/2 + 10.0
flash_pos_y = width/2 - 15.0

side_slot_length = 30.0
side_slot_height = 4.0
side_slot_pos_x = -length/2 + 35.0

bottom_port_width = 12.0
bottom_port_height = 6.0

power_port_width = 10.0
power_port_height = 5.0
power_port_pos_x = length/2 - 20.0

headphone_dia = 4.5
headphone_pos_z = height/2  # Centered on wall height

# --- Geometry Construction ---

# 1. Base Shape: A rounded rectangle extruded to height
base = (
    cq.Workplane("XY")
    .rect(length, width)
    .extrude(height)
    .edges("|Z")
    .fillet(fillet_radius)
)

# 2. Hollow out the inside to create the shell
shell = base.faces(">Z").shell(-wall_thickness)

# 3. Create the square camera cutout on the back face
# We work on the bottom face (Z=0) but we need to cut through
# The shell operation moved the bottom to Z=0 and walls up.
# Let's target the inner floor which is at Z = wall_thickness? 
# Actually, easier to cut from the very bottom (Z=0) upwards.

# Back face features (Camera square + Circular hole)
back_cuts = (
    cq.Workplane("XY")
    .workplane(offset=0) # Bottom of the case
    # Square Cutout
    .moveTo(camera_pos_x, camera_pos_y)
    .rect(camera_cutout_size, camera_cutout_size)
    # Circular Cutout (Flash/Sensor?)
    .moveTo(flash_pos_x, flash_pos_y)
    .circle(flash_dia/2)
    # Another rectangular cutout seen on the far right bottom (in image orientation)
    .moveTo(power_port_pos_x, -width/2 + 10) # Approximate pos based on image
    .rect(power_port_width, power_port_height) # Actually this looks like a slot on the face
    .extrude(wall_thickness * 2, combine=False) # Extrude enough to cut through bottom
)

# 4. Side Wall Cutouts

# Long slot on the "top" side wall (relative to image orientation)
side_cut_top = (
    cq.Workplane("XZ")
    .workplane(offset=width/2)
    .moveTo(side_slot_pos_x, height/2) # Centered vertically on wall
    .rect(side_slot_length, side_slot_height)
    .extrude(-wall_thickness * 2, combine=False)
)

# Small rectangular port on the "bottom" short wall (right side of image)
end_cut_right = (
    cq.Workplane("YZ")
    .workplane(offset=length/2)
    .moveTo(width/4, height/2) # Offset from center
    .rect(bottom_port_width, bottom_port_height)
    .extrude(-wall_thickness * 2, combine=False)
)

# Small circular port on the corner/side (Headphone jack?) - Left side of image
# This looks like it cuts through the fillet or near the corner on the short face
end_cut_left_circ = (
    cq.Workplane("YZ")
    .workplane(offset=-length/2)
    .moveTo(width/2 - fillet_radius, height/2) # Near the top corner
    .circle(headphone_dia/2)
    .extrude(wall_thickness * 3, combine=False)
)

# Rectangular slot on the bottom face (near the right edge in image)
bottom_face_slot = (
    cq.Workplane("XY")
    .moveTo(length/2 - 25, -width/2 + 12)
    .rect(15, 6)
    .extrude(wall_thickness * 2, combine=False)
)


# --- Combine Operations ---

result = (
    shell
    .cut(back_cuts)
    .cut(side_cut_top)
    .cut(end_cut_right)
    .cut(end_cut_left_circ)
    .cut(bottom_face_slot)
)