import cadquery as cq

# --- Parametric Dimensions ---
u_section_length = 70.0      # Length of the U-channel section
base_section_length = 35.0   # Length of the solid rectangular base
part_width = 15.0            # Overall width
u_section_height = 14.0      # Height of the U-channel walls
base_section_height = 9.0    # Height of the solid base
wall_thickness = 2.5         # Thickness of the side and back walls
floor_thickness = 4.0        # Thickness of the U-channel floor
tab_size = 3.0               # Size of the small tab feature

# --- Modeling ---

# 1. Create the U-Channel Section (Left part)
# Create the main block for the U-section
# Aligned to start at X=0, centered on Y, sitting on Z=0
u_part = cq.Workplane("XY").box(
    u_section_length, 
    part_width, 
    u_section_height, 
    centered=(False, True, False)
)

# Calculate parameters for the slot
slot_len = u_section_length - wall_thickness
slot_w = part_width - (2 * wall_thickness)
cut_depth = u_section_height - floor_thickness

# Cut the slot from the top face
# We shift the center of the cut rectangle to align it with the open end (X=0)
# Center of face is at u_section_length/2. Center of slot needs to be at slot_len/2.
x_offset = (slot_len / 2.0) - (u_section_length / 2.0)

u_part = (
    u_part.faces(">Z")
    .workplane()
    .center(x_offset, 0)
    .rect(slot_len, slot_w)
    .cutBlind(-cut_depth)
)

# 2. Create the Base Section (Right part)
# Creates a solid block starting at the end of the U-section
base_part = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .transformed(offset=(u_section_length, 0, 0))
    .box(base_section_length, part_width, base_section_height, centered=(False, True, False))
)

# 3. Create the Tab Feature
# A small cube located at the top-far-right corner of the base section
# Coordinates calculated to place the tab flush with the outer edges
tab_x = u_section_length + base_section_length - (tab_size / 2.0)
tab_y = (part_width / 2.0) - (tab_size / 2.0)
tab_z = base_section_height + (tab_size / 2.0)

tab_part = (
    cq.Workplane("XY")
    .box(tab_size, tab_size, tab_size, centered=(True, True, True))
    .translate((tab_x, tab_y, tab_z))
)

# --- Final Assembly ---
# Combine all geometries into a single solid
result = u_part.union(base_part).union(tab_part)