import cadquery as cq

# --- Parametric Dimensions ---
# Overall box dimensions
box_height = 80.0
box_width = 70.0
box_thickness = 20.0
wall_thickness = 2.0

# Compartment/Slot details
num_compartments = 3
compartment_gap = wall_thickness
# Calculate width of a single compartment based on overall width
compartment_width = (box_width - (num_compartments + 1) * wall_thickness) / num_compartments
compartment_depth = 12.0 # Depth of the cutout from the front face

# Upper lip details
lip_overhang = 2.0
lip_height = 2.0 # Thickness of the top ledge

# Vent slot details (bottom section)
vent_slot_width = 2.0
vent_slot_height = 40.0
vent_slot_spacing = 6.0
num_vents = 7

# Inner slot details (inside the compartments)
inner_slot_width = 1.5
inner_slot_height = 15.0
inner_slot_spacing = 4.0

# Fillet radius
fillet_radius = 2.0

# --- Geometry Construction ---

# 1. Create the main body block
main_body = cq.Workplane("XY").box(box_width, box_thickness, box_height)

# 2. Hollow out the main body to create the shell
# Instead of a simple shell, we'll cut the compartments to control the internal walls better.
# First, let's create the solid block and fillet the vertical edges
main_body = main_body.edges("|Z").fillet(fillet_radius)

# 3. Create the top compartments
# We need to cut three rectangular pockets into the top.
# The pockets go deep, but leave a bottom floor. Let's assume the floor is 5mm thick.
pocket_depth = box_height - 5.0 

# To create the "overhanging lip" effect seen in the image, we can approach this in two ways:
# A. Cut the pockets slightly smaller, then cut a larger opening at the very top.
# B. Create a lid and fuse it.
# Let's go with the subtraction method.

# Define the compartment centers
# Spacing between centers
center_pitch = compartment_width + wall_thickness
start_x = -((num_compartments - 1) * center_pitch) / 2.0

compartments = cq.Workplane("XY")

for i in range(num_compartments):
    x_pos = start_x + (i * center_pitch)
    # Cut the main deep pocket
    # The image shows the pocket is mostly rectangular.
    # We need to consider the wall thickness.
    
    # Inner pocket dimensions (the hollow part)
    inner_w = compartment_width
    inner_t = box_thickness - 2 * wall_thickness
    
    # Create the cutting solid for the pocket
    pocket = (
        cq.Workplane("XY")
        .workplane(offset=box_height/2) # Start at top face
        .center(x_pos, 0)
        .rect(inner_w, inner_t)
        .extrude(-pocket_depth)
    )
    main_body = main_body.cut(pocket)

# 4. Create the front face cutouts (the rectangular openings at the top front)
# The image shows square/rectangular openings on the front face corresponding to the top pockets.
front_cutout_height = 20.0 # Height of the opening
front_cutout_depth = 5.0   # How far back it goes (or just through the wall)

for i in range(num_compartments):
    x_pos = start_x + (i * center_pitch)
    
    # Position: Top of box, move down slightly, on the front face
    cutout = (
        cq.Workplane("XZ")
        .workplane(offset=box_thickness/2) # Front face
        .center(x_pos, box_height/2 - front_cutout_height/2 - lip_height)
        .rect(compartment_width, front_cutout_height)
        .extrude(-wall_thickness * 2) # Cut into the box
    )
    main_body = main_body.cut(cutout)

# 5. Add the "Lid" or Lip geometry
# The image shows a rim around the top openings. 
# It looks like the main block is one piece, but the top edge is distinct.
# Let's refine the top face. The simple cut previously made straight walls.
# The image shows a slight overhang. We can achieve this by adding a "cap" plate
# with smaller holes, or by modifying the cut logic. 
# Looking closely, it looks like a standard wall thickness, but the front face is cut away.
# The previous step (4) achieved the front cutout.

# 6. Create the Vertical Vent Slots (Bottom section)
# These are on the front face, below the compartments.
vent_start_y = -10.0 # Position relative to center
vent_center_pitch = vent_slot_spacing + vent_slot_width
vent_start_x = -((num_vents - 1) * vent_center_pitch) / 2.0

for i in range(num_vents):
    vx = vent_start_x + (i * vent_center_pitch)
    vent = (
        cq.Workplane("XZ")
        .workplane(offset=box_thickness/2)
        .center(vx, vent_start_y)
        .slot2D(vent_slot_height, vent_slot_width, 90) # Vertical slot
        .extrude(-wall_thickness * 3) # Cut through front wall
    )
    main_body = main_body.cut(vent)

# 7. Create the Inner Slots (Inside the top compartments)
# These are small slots visible on the back wall inside the pockets.
# We'll cut these from the front, going through the back wall or just partially into it.
# The image suggests they are on the back wall of the compartment.

inner_slot_start_y = box_height/2 - front_cutout_height/2 - lip_height # Align generally with top area
slots_per_comp = 2
slot_pitch = inner_slot_spacing + inner_slot_width

for i in range(num_compartments):
    comp_x = start_x + (i * center_pitch)
    slot_start_x = comp_x - ((slots_per_comp - 1) * slot_pitch) / 2.0
    
    for j in range(slots_per_comp):
        sx = slot_start_x + (j * slot_pitch)
        
        inner_slot = (
            cq.Workplane("XZ")
            .workplane(offset=-box_thickness/2 + wall_thickness) # Inside back face approximately
            .center(sx, inner_slot_start_y)
            .rect(inner_slot_width, inner_slot_height)
            .extrude(wall_thickness * 2) # Cut outwards or through
        )
        # To make sure we cut the back wall of the compartment
        # Let's just cut through the whole object at that specific Y height and restricted X/Z
        
        # Better approach: Cut from back face forward
        inner_slot_cut = (
             cq.Workplane("XZ")
            .workplane(offset=-box_thickness/2) # Back face
            .center(sx, inner_slot_start_y)
            .rect(inner_slot_width, inner_slot_height)
            .extrude(wall_thickness * 2) # Cut into the box
        )
        # Only apply if it makes sense visually (the image shows slots inside). 
        # Actually looking at the image, these slots are on the BACK wall of the compartment.
        main_body = main_body.cut(inner_slot_cut)


result = main_body