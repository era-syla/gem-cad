import cadquery as cq

# --- Parameter Definition ---
# Main horizontal plate
plate_width = 150.0
plate_depth = 120.0
plate_thickness = 15.0

# Holes on the main plate
hole_diameter = 6.0
hole_margin_side = 10.0
hole_margin_frontback = 10.0

# Side vertical plates
side_plate_width = 15.0
side_plate_height = 60.0
side_plate_length = 120.0  # Same as plate_depth
side_plate_offset = 10.0   # Gap between main plate and side plates

# Mounting holes/slots on the right side plate
side_hole_diameter = 6.0
side_hole_margin_v = 10.0  # Vertical margin from top/bottom
side_hole_margin_h = 7.5   # Horizontal margin (centered in width)
slot_width = 6.0
slot_length = 30.0

# --- Geometry Construction ---

# 1. Main Horizontal Plate
# We create a base rectangle and extrude it.
main_plate = (
    cq.Workplane("XY")
    .box(plate_width, plate_depth, plate_thickness)
)

# Calculate hole positions for the main plate
# The image shows holes along the left and right edges.
# Left side holes (3 visible)
left_x = -(plate_width / 2) + hole_margin_side
# Right side holes (3 visible)
right_x = (plate_width / 2) - hole_margin_side

y_positions = [
    -(plate_depth / 2) + hole_margin_frontback,
    0,
    (plate_depth / 2) - hole_margin_frontback
]

# Create list of points for the holes
hole_pts = []
for y in y_positions:
    hole_pts.append((left_x, y))
    hole_pts.append((right_x, y))

# Cut the holes in the main plate
main_plate = (
    main_plate
    .faces(">Z")
    .workplane()
    .pushPoints(hole_pts)
    .hole(hole_diameter)
)

# 2. Right Side Plate (the one with slots and holes)
# Positioned to the right of the main plate with a gap
right_plate_center_x = (plate_width / 2) + side_plate_offset + (side_plate_width / 2)

right_plate = (
    cq.Workplane("XY")
    .workplane(offset=side_plate_height/2 - plate_thickness/2) # Align bottom roughly or center vertically based on design intent. 
    # Looking at the image, the side plates seem to be centered vertically relative to the main plate's Z? 
    # Or maybe the bottoms align? Let's assume the main plate sits roughly in the middle height of the side plates.
    .center(right_plate_center_x, 0)
    .box(side_plate_width, side_plate_length, side_plate_height)
)

# Add holes to the faces of the side plate
# Based on the image, the "Right" plate in the image is actually the one in the back right. 
# It has holes on its small face (ends) and slots on its large face.

# Let's target the inner large face for slots
right_plate = (
    right_plate
    .faces("-X") # Inner face facing the main plate
    .workplane()
    # Define slot positions. It looks like two vertical slots.
    .pushPoints([
        (side_plate_length/4, 0), 
        (-side_plate_length/4, 0)
    ])
    .slot2D(slot_length, slot_width, 90) # Vertical slots
    .cutBlind(-side_plate_width) # Cut through
)

# Add corner holes on the large face of the right plate
# The image shows 4 holes in the corners of the right plate.
corner_pts = [
    (side_plate_length/2 - 10, side_plate_height/2 - 10),
    (side_plate_length/2 - 10, -(side_plate_height/2 - 10)),
    (-(side_plate_length/2 - 10), side_plate_height/2 - 10),
    (-(side_plate_length/2 - 10), -(side_plate_height/2 - 10)),
]

right_plate = (
    right_plate
    .faces("-X")
    .workplane()
    .pushPoints(corner_pts)
    .hole(side_hole_diameter)
)


# 3. Left Side Plate (the one in the foreground right of image)
# Actually, looking at the isometric view:
# The large flat plate is on the left.
# There are two vertical bars.
# One vertical bar is "attached" or close to the front-right corner of the main plate area.
# The other vertical bar is further back.
# Wait, let's re-interpret the image.
# It looks like an exploded view or an assembly.
# Object 1: Large horizontal plate.
# Object 2: Vertical plate in the foreground (Solid, but has holes on the end face).
# Object 3: Vertical plate in the background (Has slots and holes on the face).

# Let's build the "Foreground" vertical plate.
foreground_plate_center_x = (plate_width / 2) + side_plate_offset + (side_plate_width / 2)
# Shifting it in Y to match the "exploded" look or assembly position.
# It seems to be aligned with the front edge of the main plate.
foreground_plate_y_shift = -(plate_depth / 2) + (side_plate_length / 2) 

# Actually, the image shows the vertical plates are aligned with the depth of the main plate?
# No, the foreground plate looks shorter or just cut off? No, let's assume standard lengths.
# Let's position the foreground plate.
foreground_plate = (
    cq.Workplane("XY")
    .workplane(offset=side_plate_height/2 - plate_thickness/2)
    .center(right_plate_center_x - 50, -plate_depth/2 - 20) # Move it arbitrarily for the "exploded" look
    # Re-evaluating position based on shadow and perspective.
    # The foreground plate is actually adjacent to the main plate, acting like a side wall.
    # The background plate is also a side wall.
    # The image shows an assembly where the side wall is detached.
    
    # Let's model the components in a relative assembly position.
    # Foreground Vertical Block
    .center(50, 0) # Just moving it away from the main plate to match the gap in image
    .box(side_plate_width, side_plate_length, side_plate_height)
)

# Add holes to the end face of the foreground plate
foreground_plate = (
    foreground_plate
    .faces("-Y")
    .workplane()
    .pushPoints([(0, side_plate_height/2 - 10), (0, -(side_plate_height/2 - 10))])
    .hole(side_hole_diameter)
)

# Let's reconstruct to match the specific arrangement in the image exactly.
# 1. Main Plate (Left)
# 2. Foreground Vertical Plate (Right, shifted forward)
# 3. Background Vertical Plate (Right, shifted backward, has slots)

# Redefining construction for clarity and single 'result'
p1 = (
    cq.Workplane("XY")
    .box(plate_width, plate_depth, plate_thickness)
    .faces(">Z").workplane()
    .pushPoints(hole_pts)
    .hole(hole_diameter)
)

# The plate with slots (Background Right)
p2 = (
    cq.Workplane("XY")
    .box(side_plate_width, side_plate_length, side_plate_height)
    .rotate((0,0,0), (0,0,1), 0)
    .translate((plate_width/2 + 20, 20, side_plate_height/2 - plate_thickness/2)) # Shifted Right and Back
)

# Add slots to p2
p2 = (
    p2.faces("-X").workplane()
    .pushPoints([(side_plate_length/5, 0), (-side_plate_length/5, 0)])
    .slot2D(slot_length, slot_width, 90)
    .cutBlind(-side_plate_width)
)

# Add 4 corner holes to p2
p2 = (
    p2.faces("-X").workplane()
    .pushPoints([
        (side_plate_length/2 - 10, side_plate_height/2 - 10),
        (side_plate_length/2 - 10, -side_plate_height/2 + 10),
        (-side_plate_length/2 + 10, side_plate_height/2 - 10),
        (-side_plate_length/2 + 10, -side_plate_height/2 + 10),
    ])
    .hole(side_hole_diameter)
)


# The plate with end holes (Foreground Right)
p3 = (
    cq.Workplane("XY")
    .box(side_plate_width, side_plate_length, side_plate_height)
    .translate((plate_width/2 + 20, -side_plate_length - 10, side_plate_height/2 - plate_thickness/2)) # Shifted Right and Front
)

# Add holes to the end of p3 (faces -Y)
p3 = (
    p3.faces("-Y").workplane()
    .pushPoints([(0, side_plate_height/2 - 10), (0, -side_plate_height/2 + 10)])
    .hole(side_hole_diameter)
)

# Combine into a single assembly result
result = p1.union(p2).union(p3)