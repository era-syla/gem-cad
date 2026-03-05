import cadquery as cq

# --- Parameters ---
box_width = 80.0    # Width of the box (X axis)
box_depth = 60.0    # Depth of the box (Y axis)
box_height = 50.0   # Height of the box (Z axis)
material_thick = 3.0 # Thickness of the material (e.g., laser cut plywood/acrylic)

# Finger joint settings
finger_width = 10.0 # Approximate width of each finger

# Top cutout settings
slot_length = 15.0
slot_width = 4.0
slot_offset = 12.0  # Distance from center for the radial slots

# --- Helper Function for Box Joints ---
def create_finger_joints(length, thickness, finger_w, side_mode="pins"):
    """
    Creates a 2D profile of finger joints along an edge.
    length: Total length of the edge
    thickness: Material thickness (depth of the cut)
    finger_w: Target width of a finger
    side_mode: "pins" (starts with material) or "slots" (starts with gap)
    """
    # Calculate number of fingers to fit roughly the target width
    n_fingers = int(length // finger_w)
    # Ensure odd number for symmetry if possible, or adjust logic
    if n_fingers % 2 == 0:
        n_fingers -= 1
    if n_fingers < 3: n_fingers = 3
    
    actual_finger_w = length / n_fingers
    
    # Create the base wire
    pts = []
    
    # Starting point
    x = -length / 2.0
    y = 0
    pts.append((x, y))
    
    is_pin = (side_mode == "pins")
    
    for i in range(n_fingers):
        if is_pin:
            # Draw a pin (material sticks out)
            pts.append((x, thickness))
            x += actual_finger_w
            pts.append((x, thickness))
        else:
            # Draw a slot (gap) - actually just moving along the base line
            # effectively cutting into the plate if we subtract, or forming the edge
            pts.append((x, 0)) # Down/Stay
            x += actual_finger_w
            pts.append((x, 0)) # Up/Stay
            
        is_pin = not is_pin
        
    pts.append((length / 2.0, 0))
    
    # Close the shape to make a cutter or plate base
    # We will make a full rectangular plate and subtract the "negative" fingers
    # or build the "positive" shape.
    # Let's try a different approach: Build the plate, then cut.
    return actual_finger_w

# --- Construction ---

# 1. Bottom Plate
# The bottom needs tabs on all 4 sides. 
# Let's assume Front/Back cover Sides, so Front/Back get pins on X, slots on Z?
# Actually, looking at the image:
# - Top/Bottom plates have PINS on all 4 edges.
# - Front/Back plates have SLOTS on Top/Bottom edges, PINS on Left/Right.
# - Left/Right plates have SLOTS on all 4 edges.
# (This is a standard laser-cut box topology)

# Recalculate finger counts/widths to ensure mating
# X-axis fingers (Front/Back width)
n_fingers_x = int(box_width // finger_width) | 1 # Force odd
finger_w_x = box_width / n_fingers_x

# Y-axis fingers (Side width)
n_fingers_y = int(box_depth // finger_width) | 1
finger_w_y = box_depth / n_fingers_y

# Z-axis fingers (Height)
n_fingers_z = int(box_height // finger_width) | 1
finger_w_z = box_height / n_fingers_z

def make_finger_cutter(length, f_width, thick, axis='X'):
    """
    Creates a solid tool to cut slots along an edge.
    length: length of the edge
    f_width: width of a single finger
    thick: thickness of material (depth of cut)
    """
    n = int(length / f_width + 0.5)
    
    # We want to cut every *other* slot.
    # Assuming standard "Pin" corners, the cuts start at index 1 (0-indexed)
    
    res = cq.Workplane("XY")
    
    # Create individual cutter blocks
    for i in range(n):
        # Determine if this segment is a cut or solid
        # For a "Pin" edge (corners present), we cut indices 1, 3, 5...
        if i % 2 == 1:
            center_pos = -length/2 + (i + 0.5) * f_width
            if axis == 'X':
                # Cut along X edge
                res = res.union(
                    cq.Workplane("XY")
                    .center(center_pos, 0)
                    .rect(f_width, thick * 3) # Oversize depth for clean cut
                    .extrude(thick * 3)       # Oversize height
                )
            elif axis == 'Y':
                res = res.union(
                    cq.Workplane("XY")
                    .center(0, center_pos)
                    .rect(thick * 3, f_width)
                    .extrude(thick * 3)
                )
    return res

def make_inverse_finger_cutter(length, f_width, thick, axis='X'):
    """
    Creates a solid tool to cut slots, but inverted pattern (cuts 0, 2, 4...)
    Used for the mating piece.
    """
    n = int(length / f_width + 0.5)
    res = cq.Workplane("XY")
    for i in range(n):
        if i % 2 == 0: # Cut evens (corners removed)
            center_pos = -length/2 + (i + 0.5) * f_width
            if axis == 'X':
                res = res.union(
                    cq.Workplane("XY")
                    .center(center_pos, 0)
                    .rect(f_width, thick * 3)
                    .extrude(thick * 3)
                )
            elif axis == 'Y':
                res = res.union(
                    cq.Workplane("XY")
                    .center(0, center_pos)
                    .rect(thick * 3, f_width)
                    .extrude(thick * 3)
                )
    return res


# -- Generate Plates --

# Top Plate (XY Plane)
# Has PINS on all sides. We start with a solid rect and cut the "even" slots?
# If corners are material, we cut 1, 3, 5... (make_finger_cutter)
top_plate = cq.Workplane("XY").rect(box_width, box_depth).extrude(material_thick)

# Cut Front/Back edges of Top Plate
cutter_top_x = make_finger_cutter(box_width, finger_w_x, material_thick, 'X')
top_plate = top_plate.cut(cutter_top_x.translate((0, box_depth/2, 0))) # Back edge
top_plate = top_plate.cut(cutter_top_x.translate((0, -box_depth/2, 0))) # Front edge

# Cut Left/Right edges of Top Plate
cutter_top_y = make_finger_cutter(box_depth, finger_w_y, material_thick, 'Y')
top_plate = top_plate.cut(cutter_top_y.translate((box_width/2, 0, 0))) # Right edge
top_plate = top_plate.cut(cutter_top_y.translate((-box_width/2, 0, 0))) # Left edge

# Add the Top Features (Cross slots)
# Center hole
top_plate = top_plate.faces(">Z").workplane().rect(slot_width, slot_length * 2 + slot_width).cutBlind(-material_thick)
top_plate = top_plate.faces(">Z").workplane().rect(slot_length * 2 + slot_width, slot_width).cutBlind(-material_thick)

# Actually, the image shows 4 distinct slots in a cross pattern, not a continuous cross.
# Let's fix that.
top_plate = cq.Workplane("XY").rect(box_width, box_depth).extrude(material_thick)
# Re-apply edge cuts
top_plate = top_plate.cut(cutter_top_x.translate((0, box_depth/2, 0)))
top_plate = top_plate.cut(cutter_top_x.translate((0, -box_depth/2, 0)))
top_plate = top_plate.cut(cutter_top_y.translate((box_width/2, 0, 0)))
top_plate = top_plate.cut(cutter_top_y.translate((-box_width/2, 0, 0)))

# Cut the 4 specific slots
# Top slot
top_plate = top_plate.faces(">Z").workplane().center(0, slot_offset).rect(slot_width, slot_length).cutBlind(-material_thick)
# Bottom slot
top_plate = top_plate.faces(">Z").workplane().center(0, -slot_offset).rect(slot_width, slot_length).cutBlind(-material_thick)
# Left slot
top_plate = top_plate.faces(">Z").workplane().center(-slot_offset, 0).rect(slot_length, slot_width).cutBlind(-material_thick)
# Right slot - This one has a piece inserted in it in the image, but the hole needs to exist
top_plate = top_plate.faces(">Z").workplane().center(slot_offset, 0).rect(slot_length, slot_width).cutBlind(-material_thick)

# Move top plate to position
top_plate = top_plate.translate((0, 0, box_height/2 - material_thick/2))


# Bottom Plate (Same as top but solid face)
bottom_plate = cq.Workplane("XY").rect(box_width, box_depth).extrude(material_thick)
bottom_plate = bottom_plate.cut(cutter_top_x.translate((0, box_depth/2, 0)))
bottom_plate = bottom_plate.cut(cutter_top_x.translate((0, -box_depth/2, 0)))
bottom_plate = bottom_plate.cut(cutter_top_y.translate((box_width/2, 0, 0)))
bottom_plate = bottom_plate.cut(cutter_top_y.translate((-box_width/2, 0, 0)))
bottom_plate = bottom_plate.translate((0, 0, -box_height/2 + material_thick/2))


# Front Plate (XZ Plane)
# Mates with Top/Bottom (needs inverted cuts on Z edges)
# Mates with Sides (needs standard cuts on X edges - vertical in this orientation)
# Front plate dimensions: Width x Height
front_plate = cq.Workplane("XZ").rect(box_width, box_height).extrude(material_thick)

# Cut Top/Bottom edges (mating with Top/Bottom plates)
# Top/Bottom plates had Pins (corners solid), so Front needs Slots (corners cut)
# This means we use make_inverse_finger_cutter
cutter_front_z = make_inverse_finger_cutter(box_width, finger_w_x, material_thick, 'X') 
# Note: 'X' axis in local XZ plane corresponds to global X
front_plate = front_plate.cut(cutter_front_z.rotate((0,0,0),(1,0,0),90).translate((0, 0, box_height/2)))
front_plate = front_plate.cut(cutter_front_z.rotate((0,0,0),(1,0,0),90).translate((0, 0, -box_height/2)))

# Cut Left/Right edges (mating with Side plates)
# Let's say Front plate has PINS on sides.
cutter_front_sides = make_finger_cutter(box_height, finger_w_z, material_thick, 'Y')
# Rotate cutter to align with vertical Z axis
# The cutter generates along Y. We need it along Z.
cutter_front_sides_rotated = cutter_front_sides.rotate((0,0,0),(1,0,0),90) 
front_plate = front_plate.cut(cutter_front_sides_rotated.translate((box_width/2, 0, 0)))
front_plate = front_plate.cut(cutter_front_sides_rotated.translate((-box_width/2, 0, 0)))

# Move Front plate to position
front_plate_final = front_plate.translate((0, -box_depth/2 + material_thick/2, 0))

# Back Plate (Copy of Front)
back_plate_final = front_plate.translate((0, box_depth/2 - material_thick/2, 0))


# Right Plate (YZ Plane)
# Mates with Top/Bottom (inverted cuts)
# Mates with Front/Back (inverted cuts)
right_plate = cq.Workplane("YZ").rect(box_depth, box_height).extrude(material_thick)

# Cut Top/Bottom edges (mating with Top/Bottom) -> Inverted (Corners removed)
cutter_side_topbot = make_inverse_finger_cutter(box_depth, finger_w_y, material_thick, 'X')
# Local X is Global Y
right_plate = right_plate.cut(cutter_side_topbot.rotate((0,0,0),(0,1,0),-90).translate((0, 0, box_height/2)))
right_plate = right_plate.cut(cutter_side_topbot.rotate((0,0,0),(0,1,0),-90).translate((0, 0, -box_height/2)))

# Cut Front/Back edges (mating with Front/Back) -> Inverted (Corners removed)
cutter_side_vert = make_inverse_finger_cutter(box_height, finger_w_z, material_thick, 'Y')
# Local Y is Global Z. Cutter is along Y. Just need to rotate to plane.
right_plate = right_plate.cut(cutter_side_vert.rotate((0,0,0),(0,1,0),-90).translate((0, box_depth/2, 0)))
right_plate = right_plate.cut(cutter_side_vert.rotate((0,0,0),(0,1,0),-90).translate((0, -box_depth/2, 0)))

# Move Right Plate
right_plate_final = right_plate.translate((box_width/2 - material_thick/2, 0, 0))

# Left Plate (Copy of Right)
left_plate_final = right_plate.translate((-box_width/2 + material_thick/2, 0, 0))


# Small inserted tab in the top
inserted_tab = (
    cq.Workplane("XY")
    .rect(slot_length, slot_width)
    .extrude(10) # Arbitrary height sticking out
    .translate((slot_offset, 0, box_height/2 + 2)) # Position in the right slot
)


# Combine all parts
result = (
    top_plate
    .union(bottom_plate)
    .union(front_plate_final)
    .union(back_plate_final)
    .union(right_plate_final)
    .union(left_plate_final)
    .union(inserted_tab)
)