import cadquery as cq

# --- Parameter Definitions ---
# Main Plate Dimensions
plate_width = 100.0
plate_height = 100.0
plate_thickness = 2.0

# Circular Holes Parameters (Top Row)
hole_diameter_large = 6.0
hole_diameter_small = 4.0
top_hole_y_offset = 35.0  # Distance from center to top holes
# Coordinates relative to center
top_holes_coords = [
    (-35.0, top_hole_y_offset),
    (-10.0, top_hole_y_offset),
    (15.0, top_hole_y_offset),
    (30.0, 42.0) # The one slightly higher and to the right
]

# Bottom Hole Parameter
bottom_hole_y_offset = -35.0
bottom_hole_x_offset = -10.0

# Slot Parameters (Top Right)
slot_width = 2.0
slot_length = 6.0
# Coordinates for slots (center points)
slot_coords = [
    (38.0, 32.0), # Vertical slot
    (45.0, 40.0), # Horizontal top
    (45.0, 25.0), # Horizontal bottom
]

# Large Cutout Parameters (Bottom Right)
# The shape is roughly a rectangle with a stepped top and bottom
# Let's define the points for a polygon cut relative to the bottom right corner area
# We will sketch this relative to the plate center to make it easier to place.
# The cutout is situated in the bottom-right quadrant.
cutout_center_x = 25.0
cutout_center_y = -20.0
cutout_main_w = 40.0
cutout_main_h = 40.0
cutout_neck_w = 15.0
cutout_neck_h = 10.0 # Height of the little tab/extension

# --- Modeling ---

# 1. Create the base plate
result = cq.Workplane("XY").box(plate_width, plate_height, plate_thickness)

# 2. Add Top Circular Holes
for x, y in top_holes_coords:
    # Use different diameters based on position if needed, 
    # visually the top right one is slightly larger, others look uniform.
    d = hole_diameter_large if x > 20 else hole_diameter_small
    result = result.faces(">Z").workplane().center(x, y).hole(d)

# 3. Add Bottom Circular Hole
result = result.faces(">Z").workplane().center(bottom_hole_x_offset, bottom_hole_y_offset).hole(hole_diameter_small)

# 4. Add Small Slots (Top Right)
# Vertical slot
result = result.faces(">Z").workplane().center(slot_coords[0][0], slot_coords[0][1]).slot2D(slot_length, slot_width, angle=90).cutThruAll()
# Horizontal top slot
result = result.faces(">Z").workplane().center(slot_coords[1][0], slot_coords[1][1]).slot2D(slot_length, slot_width, angle=0).cutThruAll()
# Horizontal bottom slot
result = result.faces(">Z").workplane().center(slot_coords[2][0], slot_coords[2][1]).slot2D(slot_length, slot_width, angle=0).cutThruAll()

# 5. Create the Complex Cutout
# We will draw the profile of the cutout. 
# Looking at the image:
# It's a large rectangle.
# It has a rectangular protrusion on top.
# It has a rectangular protrusion on the bottom (or the main body is wider than the bottom part).
# Let's define it as a polygon.

# Rough coordinates relative to the center of the cutout shape
p1 = (-15, -20) # Bottom left
p2 = (5, -20)   # Bottom inner corner
p3 = (5, -28)   # Bottom protrusion start (down) - actually looking at image, it's a cutout on the bottom edge of the shape
                # Let's re-evaluate the shape. It looks like a "plus" sign or "T" shape combined.
                # Let's trace the outline counter-clockwise starting from bottom-left of the cutout.

# Refined shape definition:
# The cutout is on the right side.
# Let's define absolute coordinates relative to the plate center (0,0)
# Plate is -50 to 50 in X, -50 to 50 in Y.

cutout_x_start = 0.0
cutout_x_mid = 20.0
cutout_x_end = 45.0
cutout_y_bottom = -40.0
cutout_y_low_step = -25.0
cutout_y_high_step = 5.0
cutout_y_top = 20.0

# Let's trace the points based on visual estimation
pts = [
    (cutout_x_start, cutout_y_low_step),  # Left-bottom corner
    (cutout_x_mid, cutout_y_low_step),    # Step in
    (cutout_x_mid, cutout_y_bottom),      # Down
    (cutout_x_end, cutout_y_bottom),      # Bottom right
    (cutout_x_end, cutout_y_low_step),    # Up (right edge continues higher but lets stop here for symmetry check)
    (cutout_x_end, 0),                    # Right edge mid
    (cutout_x_end, 10),                   # Right edge
    (cutout_x_mid, 10),                   # Step in top
    (cutout_x_mid, 20),                   # Up top
    (cutout_x_start + 15, 20),            # Top left-ish
    (cutout_x_start + 15, 10),            # Down
    (cutout_x_start, 10),                 # Left 
    (cutout_x_start, cutout_y_low_step)   # Close loop
]

# The shape seems to be a main rectangle with a smaller rectangle on top and bottom removed/added.
# Let's try a union of rectangles approach for cleaner code.
# Main body of cutout
c_main = cq.Workplane("XY").workplane(offset=plate_thickness/2).center(25, -15).rect(45, 40)
# Top tab cutout
c_top = cq.Workplane("XY").workplane(offset=plate_thickness/2).center(25, 10).rect(15, 15)
# Bottom tab cutout (actually the image shows the cutout goes closer to the edge)
c_bot = cq.Workplane("XY").workplane(offset=plate_thickness/2).center(35, -35).rect(25, 20)

# Actually, drawing the specific polygon is safer.
# Let's look at the "stepped" nature.
# It looks like a central block, with a block on top, and the bottom right corner extended.
# Let's define the points relative to a local reference for the cutout.
cutout_points = [
    (0, 0),         # Start bottom-left of main block
    (20, 0),        # Right to first step
    (20, -10),      # Down
    (40, -10),      # Right (Bottom Right extremity)
    (40, 40),       # Up (Top Right extremity)
    (25, 40),       # Left
    (25, 50),       # Up (Top tab)
    (10, 50),       # Left (Top tab width)
    (10, 40),       # Down
    (0, 40),        # Left
    (0, 0)          # Close
]

# Adjust positioning to match image
# The shape is in the bottom right quadrant.
# Let's offset these points so (0,0) is roughly the bottom-left corner of the cutout on the plate.
# Visually, the bottom-left corner of the cutout is at X=0, Y=-30 (relative to plate center)
x_shift = -5.0
y_shift = -35.0

final_pts = [(p[0] + x_shift, p[1] + y_shift) for p in cutout_points]

# Perform the Cut
result = result.faces(">Z").workplane().polyline(final_pts).close().cutThruAll()

# --- Export/Show ---
# show_object(result)