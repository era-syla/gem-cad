import cadquery as cq

# --- Parameters ---
# Overall dimensions
length = 100.0
width = 40.0
base_thickness = 5.0

# Raised side rails
rail_width = 8.0
rail_height = 2.0  # Height above base
total_thickness = base_thickness + rail_height

# Central cutout/slot details
# It appears there's a wide central channel.
# Let's define the channel width implicitly by the rail width.
# There are also specific rectangular pockets inside the channel near the ends.
pocket_length = 25.0
pocket_width = 8.0
pocket_depth = 1.0 # Depth cut into the base
pocket_offset_from_center = 20.0 # Distance from center of part to center of pocket

# Side notches
notch_width = 8.0
notch_depth = 5.0

# Mounting holes
hole_diameter = 3.5
hole_dx = length/2 - 5.0 # Distance from center to hole center along X
hole_dy = width/2 - rail_width/2 # Center the hole on the rail

# --- Modeling ---

# 1. Start with the main block (the full bounding box)
# We will cut away from this or build up. Building up from base is often cleaner.

# Base plate
base = cq.Workplane("XY").box(length, width, base_thickness)

# 2. Add the side rails
# Create a sketch for the rails on top of the base
rails = (
    base.faces(">Z").workplane()
    .rect(length, width - 2*rail_width) # The area to NOT extrude (the middle)
    .extrude(rail_height) # This creates a block in the middle, wait.
)
# Let's try a different approach: Make the full block and cut the middle channel.
part = cq.Workplane("XY").box(length, width, total_thickness)

# Cut the main central channel
# The channel goes through the whole length
channel_width = width - 2 * rail_width
part = part.faces(">Z").workplane().rect(length, channel_width).cutBlind(-rail_height)

# 3. Cut the rectangular pockets in the channel floor
# There are two pockets, symmetric about the center.
part = (
    part.faces(">Z").workplane(offset=-rail_height) # Work on the channel floor
    .pushPoints([(pocket_offset_from_center, 0), (-pocket_offset_from_center, 0)])
    .rect(pocket_length, pocket_width)
    .cutBlind(-pocket_depth)
)

# 4. Cut the side notches
# These are rectangular cutouts from the sides into the center
part = (
    part.faces(">Z").workplane() # Top plane
    .pushPoints([(0, width/2), (0, -width/2)]) # Points on the side edges
    .rect(notch_width, notch_depth * 2) # *2 to ensure it cuts through the edge from the center point
    .cutBlind(-total_thickness)
)

# 5. Add mounting holes
# 4 holes, one in each corner on the rails
holes_x = [hole_dx, -hole_dx]
holes_y = [hole_dy, -hole_dy]
hole_centers = [(x, y) for x in holes_x for y in holes_y]

part = (
    part.faces(">Z").workplane()
    .pushPoints(hole_centers)
    .hole(hole_diameter)
)

result = part