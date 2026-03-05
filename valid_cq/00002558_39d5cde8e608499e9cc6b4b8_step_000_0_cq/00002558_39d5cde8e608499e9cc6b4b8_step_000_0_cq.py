import cadquery as cq

# This code creates a simplified representation of the complex assembly shown in the image.
# The image depicts a highly intricate mechanism, possibly an exploded view of an automation
# jig or fixture. Recreating every specific detail without precise engineering drawings
# is impossible. Instead, this script generates the major forms and layout:
# 1. A standalone large block (bottom left)
# 2. A main base assembly with linear rails and blocks
# 3. An upright vertical plate assembly (top left)
# 4. A sliding carriage mechanism (center)

# --- Parameters ---
# Standalone Block
iso_block_L = 80
iso_block_W = 40
iso_block_H = 40

# Main Base Structure
base_L = 150
base_W = 100
base_H = 50

# Linear Rail Params
rail_length = 200
rail_width = 15
rail_height = 10

# Carriage Plate
carriage_L = 80
carriage_W = 60
carriage_thickness = 10

# Vertical Plate Assembly
vert_plate_H = 80
vert_plate_W = 50
vert_plate_T = 5

# --- 1. Isolated Block (Bottom Left) ---
# Positioned relative to the main assembly
isolated_block = (
    cq.Workplane("XY")
    .box(iso_block_L, iso_block_W, iso_block_H)
    .translate((-150, -100, 0))  # Move away from center
)

# --- 2. Main Base Assembly (Right Side) ---
# Create the large block on the right
main_base = (
    cq.Workplane("XY")
    .box(base_L, base_W, base_H)
    .translate((100, 0, 0))
)

# Add some details to the main base to mimic the machined look
main_base = (
    main_base
    .faces(">Z").workplane()
    .rect(base_L - 20, base_W - 20).cutBlind(-10) # Pocket
)

# --- 3. Linear Rails & Mechanism (Center) ---
# Rail 1
rail1 = (
    cq.Workplane("XY")
    .box(rail_length, rail_width, rail_height)
    .translate((0, -30, 20)) # Lifted up slightly
)

# Rail 2
rail2 = (
    cq.Workplane("XY")
    .box(rail_length, rail_width, rail_height)
    .translate((0, 30, 20))
)

# Sliding Blocks on Rails
slider_block_dim = 25
slider1 = (
    cq.Workplane("XY")
    .box(slider_block_dim, slider_block_dim+10, slider_block_dim)
    .translate((-20, -30, 20 + slider_block_dim/2))
)
slider2 = (
    cq.Workplane("XY")
    .box(slider_block_dim, slider_block_dim+10, slider_block_dim)
    .translate((-20, 30, 20 + slider_block_dim/2))
)

# Central Connecting Plate (Carriage)
carriage = (
    cq.Workplane("XY")
    .box(carriage_L, carriage_W, carriage_thickness)
    .translate((-20, 0, 45)) # Resting on sliders
)

# Add cutout to carriage
carriage = (
    carriage.faces(">Z").workplane()
    .rect(40, 30).cutBlind(-5)
)

# Add a black component (likely a cylinder or sensor) extending out
sensor_rod = (
    cq.Workplane("YZ")
    .circle(5)
    .extrude(100)
    .translate((-50, 0, 40))
    .rotate((0,0,0), (0,1,0), -90) # Orient along X
    .translate((-20, 0, 0))
)


# --- 4. Vertical Plate Assembly (Top Left exploded part) ---
vertical_structure = (
    cq.Workplane("YZ")
    .box(vert_plate_W, vert_plate_T, vert_plate_H)
    .translate((-80, 80, 60))
)

# Add mounting blocks to vertical structure
v_mount_top = (
    cq.Workplane("XY")
    .box(20, 60, 20)
    .translate((-80, 80, 90))
)
v_mount_bot = (
    cq.Workplane("XY")
    .box(20, 60, 20)
    .translate((-80, 80, 30))
)

# Small floating components (exploded view items)
small_cube1 = cq.Workplane("XY").box(10,10,10).translate((-100, 100, 80))
small_cyl1 = cq.Workplane("XY").circle(5).extrude(10).translate((-120, 90, 70))


# --- 5. Upper Frame Structure (Above main rails) ---
# A frame that looks like it slides or holds the top part
upper_frame_bar1 = (
    cq.Workplane("XY")
    .box(120, 10, 10)
    .translate((20, -40, 80))
)
upper_frame_bar2 = (
    cq.Workplane("XY")
    .box(120, 10, 10)
    .translate((20, 40, 80))
)
upper_frame_cross = (
    cq.Workplane("XY")
    .box(20, 90, 10)
    .translate((70, 0, 80))
)

# --- Combine All Parts ---
# We use union to combine them into a single object for the 'result' variable
# In a real assembly, these would be separate bodies.

result = (
    isolated_block
    .union(main_base)
    .union(rail1)
    .union(rail2)
    .union(slider1)
    .union(slider2)
    .union(carriage)
    .union(sensor_rod)
    .union(vertical_structure)
    .union(v_mount_top)
    .union(v_mount_bot)
    .union(small_cube1)
    .union(small_cyl1)
    .union(upper_frame_bar1)
    .union(upper_frame_bar2)
    .union(upper_frame_cross)
)