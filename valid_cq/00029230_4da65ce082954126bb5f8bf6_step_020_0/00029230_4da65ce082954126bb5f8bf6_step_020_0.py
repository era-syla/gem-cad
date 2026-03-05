import cadquery as cq

# --- Parametric Dimensions ---
length = 160.0          # Total length of the base bar
height = 25.0           # Height of the part
bar_thickness = 12.0    # Thickness of the front base bar

block_width = 30.0      # Width of the bearing blocks
block_depth = 22.0      # Depth the blocks protrude from the back
block_spacing = 100.0   # Center-to-center distance between blocks

shaft_diam = 12.0       # Diameter of the vertical shaft holes
slit_width = 1.5        # Width of the clamping slit
clamp_hole_diam = 4.2   # Diameter of the horizontal clamping screw holes
clamp_offset = 6.0      # Offset of clamp hole behind shaft center

slot_length = 14.0      # Length of mounting slots
slot_width = 6.5        # Width of mounting slots
slot_spacing = 130.0    # Spacing between mounting slots

# --- Derived Values ---
block_x = block_spacing / 2.0
slot_x = slot_spacing / 2.0
# Calculate Y center of the block.
# Bar extends Y from -bar_thickness/2 to +bar_thickness/2.
# Blocks attach to back face (+bar_thickness/2) and extend by block_depth.
block_center_y = (bar_thickness / 2.0) + (block_depth / 2.0)

# --- Modeling ---

# 1. Base Body
# Create the main rectangular bar centered at origin
base = cq.Workplane("XY").box(length, bar_thickness, height)

# Create a single block geometry
block_geo = cq.Workplane("XY").box(block_width, block_depth, height)

# Position and unite blocks to the base
right_block = block_geo.translate((block_x, block_center_y, 0))
left_block = block_geo.translate((-block_x, block_center_y, 0))

result = base.union(right_block).union(left_block)

# 2. Vertical Shaft Holes
# Cut vertical holes through the center of each block
result = result.faces(">Z").workplane().pushPoints([
    (block_x, block_center_y),
    (-block_x, block_center_y)
]).hole(shaft_diam)

# 3. Clamping Slits
# Cut a thin slit from the back face into the shaft hole.
# We position a cutting rectangle centered at the back edge of the block.
# Height of rect is block_depth, so it cuts inwards exactly to the hole center.
slit_cut_y = block_center_y + (block_depth / 2.0)

result = result.faces(">Z").workplane().pushPoints([
    (block_x, slit_cut_y),
    (-block_x, slit_cut_y)
]).rect(slit_width, block_depth).cutThruAll()

# 4. Clamp Screw Holes
# Horizontal holes passing through the sides of the blocks to tighten the slit.
# Located behind the shaft hole.
clamp_y_pos = block_center_y + clamp_offset

# Create a cylinder tool oriented along X-axis to cut through both blocks
clamp_tool = (
    cq.Workplane("YZ")
    .workplane(offset=-length/2.0) # Start from negative X
    .moveTo(clamp_y_pos, 0)
    .circle(clamp_hole_diam / 2.0)
    .extrude(length)               # Extrude across the entire part length
)

result = result.cut(clamp_tool)

# 5. Mounting Slots
# Create slots on the front face of the main bar.
# Face <Y is the front face.
result = result.faces("<Y").workplane().pushPoints([
    (slot_x, 0),
    (-slot_x, 0)
]).slot2D(slot_length, slot_width, 0).cutThruAll()

# 'result' now contains the final geometry