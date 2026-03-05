import cadquery as cq

# --- Parameter Definitions ---

# Plate dimensions
plate_thickness = 5.0
l_leg_1_length = 100.0  # Horizontal leg
l_leg_1_width = 50.0
l_leg_2_length = 80.0   # Vertical leg
l_leg_2_width = 60.0    # Width of the vertical section

# Feature dimensions
# Square Cutout
square_cutout_size = 20.0
square_cutout_center = (10, 10) # Relative to some origin, adjusted later

# Circular Holes
large_hole_diam = 10.0
small_hole_diam = 3.0

# Slot dimensions
slot_length = 20.0
slot_width = 8.0
lobe_radius = 2.0  # Radius of the small circular cutouts at slot ends

# --- Construction Helper Functions ---

def create_lobed_slot(loc_vector, rotation=0):
    """
    Creates a single lobed slot solid to be subtracted.
    The slot consists of a central rounded rectangle and four corner lobes.
    """
    # Create the main slot body (rounded rectangle style)
    slot_body = (
        cq.Workplane("XY")
        .rect(slot_length, slot_width)
        .extrude(plate_thickness)
        .edges("|Z").fillet(slot_width/2.0 - 0.01) # Full round ends
    )
    
    # Create the lobes (small cylinders at the 'corners' of the straight section)
    # The straight section length is slot_length - slot_width
    straight_len = slot_length - slot_width
    dx = straight_len / 2.0
    dy = slot_width / 2.0
    
    lobes = (
        cq.Workplane("XY")
        .pushPoints([(-dx, dy), (dx, dy), (-dx, -dy), (dx, -dy)])
        .circle(lobe_radius)
        .extrude(plate_thickness)
    )
    
    combined_slot = slot_body.union(lobes)
    
    # Move and rotate the slot to the target location
    return combined_slot.rotate((0,0,0), (0,0,1), rotation).translate(loc_vector)

# --- Main Geometry Construction ---

# 1. Base L-Plate
# We'll construct this by unioning two rectangles or sketching the profile.
# Let's use a sketch approach for cleaner topology.
# Origin (0,0) will be at the inner corner of the L for easier relative positioning.

base_plate = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(l_leg_1_length, 0)
    .lineTo(l_leg_1_length, l_leg_1_width)
    .lineTo(-l_leg_2_width, l_leg_1_width)
    .lineTo(-l_leg_2_width, -l_leg_2_length + l_leg_1_width) # Total height down
    .lineTo(0, -l_leg_2_length + l_leg_1_width)
    .close()
    .extrude(plate_thickness)
)

# 2. Square Cutout
# Located roughly near the inner corner on the horizontal leg
square_cut = (
    cq.Workplane("XY")
    .rect(square_cutout_size, square_cutout_size)
    .extrude(plate_thickness)
    .translate((square_cutout_size/2 + 10, square_cutout_size/2 + 5, 0))
)

# 3. Circular Holes
# Large hole on the far right
large_hole_1 = (
    cq.Workplane("XY")
    .circle(large_hole_diam/2)
    .extrude(plate_thickness)
    .translate((l_leg_1_length - 20, l_leg_1_width/2, 0))
)

# Large hole near the middle/top
large_hole_2 = (
    cq.Workplane("XY")
    .circle(large_hole_diam/2)
    .extrude(plate_thickness)
    .translate((-15, 30, 0))
)

# Small holes scattered around
small_hole_locs = [
    (-35, 15),    # Near vertical slots
    (15, 10),     # Near inner corner
    (-5, 40),     # Top middle
    (-55, -5)     # Bottom leg
]

small_holes = (
    cq.Workplane("XY")
    .pushPoints(small_hole_locs)
    .circle(small_hole_diam/2)
    .extrude(plate_thickness)
)


# 4. Lobed Slots
# We will define positions and orientations and subtract them.
# Positions are estimated from the image relative to inner corner (0,0).

slots_to_cut = []

# Slot 1: Top right of vertical section (Horizontal)
slots_to_cut.append(create_lobed_slot((-10, 55, 0), rotation=0))

# Slot 2: Top left of vertical section (Horizontal)
slots_to_cut.append(create_lobed_slot((-45, 55, 0), rotation=0))

# Slot 3: Middle vertical section (Horizontal)
slots_to_cut.append(create_lobed_slot((-25, 15, 0), rotation=0))

# Slot 4: Bottom vertical leg (Horizontal) - actually the lower part of the L
# The image shows these aligned along the bottom edge of the vertical leg.
slots_to_cut.append(create_lobed_slot((-45, -15, 0), rotation=0))

# Slot 5: Far bottom vertical leg (Horizontal)
slots_to_cut.append(create_lobed_slot((-80, -15, 0), rotation=0))

# 5. Combine and Cut
result = base_plate.cut(square_cut)
result = result.cut(large_hole_1).cut(large_hole_2)
result = result.cut(small_holes)

for slot in slots_to_cut:
    result = result.cut(slot)

# Export or Display
# show_object(result) # Used in CQ-editor