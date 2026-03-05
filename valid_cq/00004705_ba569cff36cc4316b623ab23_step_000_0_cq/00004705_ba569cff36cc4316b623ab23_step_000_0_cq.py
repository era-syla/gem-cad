import cadquery as cq

# --- Parameter Definitions ---
# Main plate dimensions
plate_width = 80.0
plate_length = 50.0
plate_thickness = 3.0

# Central rectangular hole
rect_hole_width = 20.0
rect_hole_length = 10.0

# Countersunk holes
screw_hole_dist = 20.0  # Distance from center along width
screw_hole_dia = 3.5
csk_dia = 7.0
csk_angle = 90.0

# Corner Clips (U-shaped)
clip_base_width = 8.0
clip_base_length = 6.0
clip_height = 8.0
clip_thickness = 1.5
clip_gap = 2.0
clip_offset_x = (plate_width / 2) - (clip_base_width / 2) # Flush with edge roughly
clip_offset_y = (plate_length / 2) - (clip_base_length / 2)

# Side Mounting Lugs (Rounded with hole)
lug_width = 8.0
lug_height = 10.0
lug_thickness = 3.0
lug_hole_dia = 3.0
lug_offset_y = (plate_length / 2) - 3.0 # Slightly inset from edge

# --- Geometry Construction ---

# 1. Base Plate
base = cq.Workplane("XY").box(plate_width, plate_length, plate_thickness)

# 2. Central Cutout
base = base.faces(">Z").workplane().rect(rect_hole_width, rect_hole_length).cutThruAll()

# 3. Countersunk Holes
# We use cskHole which handles the drilling and countersinking
base = (
    base.faces(">Z")
    .workplane()
    .pushPoints([(-screw_hole_dist, 0), (screw_hole_dist, 0)])
    .cskHole(screw_hole_dia, csk_dia, csk_angle)
)

# 4. Corner Clips
# Strategy: Create a single clip profile and extrude it, then mirror/place at 4 corners.
# Let's define one clip at the top-right corner.
def create_clip(loc):
    return (
        cq.Workplane("XY")
        .workplane(offset=plate_thickness/2) # Start on top of the plate
        .center(loc[0], loc[1])
        .rect(clip_base_width, clip_base_length)
        .extrude(clip_height)
        # Cut the slot
        .faces(">Z").workplane()
        .rect(clip_gap, clip_base_length)
        .cutThruAll()
    )

# Coordinates for the 4 corners
clip_locs = [
    (clip_offset_x, clip_offset_y),
    (-clip_offset_x, clip_offset_y),
    (clip_offset_x, -clip_offset_y),
    (-clip_offset_x, -clip_offset_y)
]

# Create and union clips
for loc in clip_locs:
    clip = create_clip(loc)
    base = base.union(clip)


# 5. Side Mounting Lugs
# Strategy: Sketch on the top face, extrude up, fillet top, cut hole.
# These are located on the "long" edges (Y-axis bounds) based on the image.

# Define the shape for one lug
def create_lug(y_pos):
    lug = (
        cq.Workplane("XY")
        .workplane(offset=plate_thickness/2)
        .center(0, y_pos)
        .rect(lug_width, lug_thickness)
        .extrude(lug_height)
    )
    
    # Round the top
    lug = lug.edges("|Y").fillet(lug_width / 2.0 - 0.01) # Slightly less to avoid kernel issues
    
    # Cut the hole
    # Find the center of the rounded face or just project coordinates
    center_height = plate_thickness/2 + lug_height - (lug_width/2)
    lug = (
        lug.faces(">Y" if y_pos > 0 else "<Y")
        .workplane(centerOption="CenterOfMass")
        .transformed(offset=(0, lug_height/2 - lug_width/2, 0)) # Adjust to center of circle
        .circle(lug_hole_dia / 2)
        .cutThruAll()
    )
    return lug

lug_top = create_lug(lug_offset_y)
lug_bottom = create_lug(-lug_offset_y)

# Union the lugs to the base
result = base.union(lug_top).union(lug_bottom)

# Optional: Add small fillets to the base of features for realism/strength (as seen in image)
# This can be computationally expensive, so applied selectively or omitted for pure geometry.
# For this script, we return the clean boolean geometry.