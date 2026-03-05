import cadquery as cq

# --- Parameters ---

# General Dimensions
part_thickness = 4.0
fillet_radius = 1.0

# Strap Loop Section (Common to both parts roughly)
loop_width = 30.0
loop_length = 12.0
slot_width = 22.0
slot_length = 4.0
wall_thickness = (loop_width - slot_width) / 2.0

# Male Part Specifics
male_body_length = 25.0
male_tongue_length = 20.0
male_tongue_width = 16.0
rib_count = 5
rib_height = 1.0
rib_width = 2.0  # approximate width of each serration

# Female Part Specifics (The loop shown separately)
female_loop_length = 12.0
female_loop_width = 32.0


# --- Modeling the Male Part ---

# 1. Main body with two slots
# Base shape
male_base = (
    cq.Workplane("XY")
    .box(male_body_length, loop_width, part_thickness)
    .edges("|Z")
    .fillet(fillet_radius)
)

# Cut the two slots
# Slot 1
slot1 = (
    cq.Workplane("XY")
    .box(slot_length, slot_width, part_thickness * 2)
    .translate((male_body_length/4 - slot_length/2 - 1, 0, 0)) # Adjust position slightly
)
# Slot 2
slot2 = (
    cq.Workplane("XY")
    .box(slot_length, slot_width, part_thickness * 2)
    .translate((-male_body_length/4 + slot_length/2 + 1, 0, 0)) # Adjust position slightly
)

male_part_slotted = male_base.cut(slot1).cut(slot2)

# 2. The Tongue (Latch mechanism)
# It extends from the main body.
tongue = (
    cq.Workplane("XY")
    .box(male_tongue_length, male_tongue_width, part_thickness)
    .edges("|Z").fillet(fillet_radius)
    .translate((- (male_body_length/2 + male_tongue_length/2), 0, 0))
)

# 3. Ribs/Serrations on the tongue
# We create a profile for the serrations and cut or add them. Looking at image, they are added material or cuts.
# They look like triangular prisms or small ramps on top.
# Let's make a single rib shape and repeat it.

rib_shape = (
    cq.Workplane("YZ")
    .moveTo(-male_tongue_width/2, 0)
    .lineTo(male_tongue_width/2, 0)
    .lineTo(male_tongue_width/2, rib_height)
    .lineTo(-male_tongue_width/2, rib_height)
    .close()
    .extrude(rib_width)
    # Orient it correctly along X
    .rotate((0,0,0), (0,1,0), 90) # Rotate to align with X axis
    .rotate((0,0,0), (1,0,0), 90) # Rotate to stand up
)

# Place ribs
ribs = cq.Workplane("XY")
start_x = - (male_body_length/2 + male_tongue_length) + 2 # Start near the tip
for i in range(rib_count):
    # Position each rib
    rib_instance = (
        cq.Workplane("XY")
        .box(rib_width, male_tongue_width, rib_height)
        # Shift it to the top surface
        .translate((start_x + i * (rib_width + 1.5), 0, part_thickness/2 + rib_height/2))
    )
    # Let's make them triangular/ramp like for better realism
    # Actually, simpler box ribs are fine, but let's chamfer the top edge to make them "grippy"
    rib_instance = rib_instance.edges(">Z and <X").chamfer(rib_height*0.9)
    
    if i == 0:
        all_ribs = rib_instance
    else:
        all_ribs = all_ribs.union(rib_instance)

male_assembly = male_part_slotted.union(tongue).union(all_ribs)


# --- Modeling the Female Loop Part (Floating piece) ---

# This is a simple rectangular loop
female_loop = (
    cq.Workplane("XY")
    .box(female_loop_length, female_loop_width, part_thickness)
    .edges("|Z").fillet(fillet_radius)
)

female_slot = (
    cq.Workplane("XY")
    .box(slot_length, slot_width + 2, part_thickness * 2) # Slightly wider slot
)

female_part = female_loop.cut(female_slot)

# Position the female part relative to the male part as shown in the image
# It is offset in X and Y
female_part_positioned = female_part.translate((male_body_length/2 + 20, 20, 0))


# --- Combine into final result ---

result = male_assembly.union(female_part_positioned)