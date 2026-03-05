import cadquery as cq

# --- Parameters ---
# Main Body Dimensions
block_w = 45.0      # Main block width (X)
block_d = 45.0      # Main block depth (Y)
block_h = 60.0      # Main block height (Z)
ext_w = 25.0        # Top extension width (Left X)
ext_h = 12.0        # Top extension thickness
chamfer_dim = 3.0   # Vertical edge chamfer size

# Top Cylindrical Boss
boss_dia = 38.0
boss_h = 5.0
dish_rad = 12.0     # Radius of the spherical cut
dish_depth = 2.5    # Depth of the spherical cut from boss top

# Top Pattern Features
bcd = 26.0          # Bolt Circle Diameter
hole_dia_top = 5.0
cb_dia_top = 9.0
cb_depth_top = 4.0
small_hole_dia = 2.5

# Side Extension Holes
ext_hole_spacing = 13.0

# Front Face Features (Pads & Holes)
pad_size = 12.0
pad_thick = 2.0
pad_spacing_x = 26.0 # Horizontal spacing between pad centers
pad_spacing_z = 28.0 # Vertical spacing between pad centers

hole_dia_side = 5.0
cb_dia_side = 9.0
cb_depth_side = 3.5

pocket_w = 16.0
pocket_h = 8.0
pocket_depth = 1.0

# --- Geometry Construction ---

# 1. Create Main Body
# Main Block: Aligned such that Top Face is Z=0, Front Face is -Y
main_blk = (
    cq.Workplane("XY")
    .box(block_w, block_d, block_h, centered=(True, True, False))
    .translate((0, 0, -block_h))
)

# Extension Plate: Extends to the Left (-X)
ext_center_x = -block_w/2 - ext_w/2
extension = (
    cq.Workplane("XY")
    .box(ext_w, block_d, ext_h, centered=(True, True, False))
    .translate((ext_center_x, 0, -ext_h))
)

# Union and apply chamfers
# We chamfer the vertical outer edges. 
# Filter: Right side of block (X > 0) and Left side of extension (X < ext_center)
base = main_blk.union(extension)
base = base.edges("|Z").filter(
    lambda e: e.Center().x > 0 or e.Center().x < (ext_center_x + 5)
).chamfer(chamfer_dim)

# 2. Add Top Boss
boss = (
    cq.Workplane("XY")
    .circle(boss_dia / 2)
    .extrude(boss_h)
)

result = base.union(boss)

# Chamfer top rim of boss
result = result.edges(">Z").filter(lambda e: abs(e.Center().x) < 0.1).chamfer(1.0)

# 3. Top Boss Features (Holes and Dish)
boss_top_plane = result.faces(">Z").filter(lambda f: abs(f.Center().x) < 0.1).workplane()

# 5 Counterbored Holes
result = (
    boss_top_plane
    .polarArray(bcd/2, 0, 360, 5)
    .cboreHole(hole_dia_top, cb_dia_top, cb_depth_top, depth=25.0)
)

# 5 Small Holes (Interspersed)
result = (
    result.faces(">Z").workplane()
    .polarArray(bcd/2, 36, 360, 5) # Offset by 36 degrees (360/10)
    .hole(small_hole_dia, depth=15.0)
)

# Center Spherical Dish
# Calculate sphere center Z to achieve desired depth
# Sphere Z = top_z + Radius - depth
sphere_z = boss_h + dish_rad - dish_depth
sphere_cut = cq.Workplane("XY").workplane(offset=sphere_z).sphere(dish_rad)
result = result.cut(sphere_cut)

# 4. Extension Holes
# 3 Counterbored holes in a row on the extension
result = (
    result.faces(">Z").filter(lambda f: f.Center().x < -10).workplane()
    .center(ext_center_x, 0)
    .pushPoints([(0, -ext_hole_spacing), (0, 0), (0, ext_hole_spacing)])
    .cboreHole(hole_dia_top, cb_dia_top, cb_depth_top, depth=ext_h + 5)
)

# 5. Front Face Features (Pads, Holes, Pocket)
# Define coordinates relative to the face center
# Face center Z is roughly -block_h/2
py_top = pad_spacing_z / 2
py_bot = -pad_spacing_z / 2
px = pad_spacing_x / 2

pad_locs = [
    (-px, py_top), (px, py_top),   # Top Row
    (-px, py_bot), (px, py_bot)    # Bottom Row
]

# Create Pads on Front Face (-Y face)
# We workplane on the face, draw rectangles, and extrude
front_plane = result.faces("<Y").workplane().center(0, -block_h/2)

pads = (
    front_plane
    .pushPoints(pad_locs)
    .rect(pad_size, pad_size)
    .extrude(pad_thick)
)
result = result.union(pads)

# Create Holes through Pads
# Select the new front-most faces (tops of pads)
result = (
    result.faces("<Y").workplane()
    .pushPoints(pad_locs) # Locations need to match the pad centers on the new plane
    # The new plane is offset, but pushPoints works in local 2D coordinates.
    # We need to re-center the grid to match the previous logic
    .center(0, -block_h/2)
    .cboreHole(hole_dia_side, cb_dia_side, cb_depth_side)
)

# Create Middle Holes (Between top and bottom pads)
# These are recessed into the main block face.
# We must select the face BEHIND the pads.
# Front face Y = -block_d/2. Pad face Y = -block_d/2 - pad_thick.
# Select face at Y = -block_d/2
mid_hole_locs = [(-px, 0), (px, 0)]

result = (
    result.faces("|Y").filter(lambda f: abs(f.Center().y + block_d/2) < 0.1).workplane()
    .center(0, -block_h/2)
    .pushPoints(mid_hole_locs)
    .cboreHole(hole_dia_side, cb_dia_side, cb_depth_side)
)

# Create Rectangular Pocket
# Between bottom pads
pocket_loc = (0, py_bot) # Aligned with bottom row

result = (
    result.faces("|Y").filter(lambda f: abs(f.Center().y + block_d/2) < 0.1).workplane()
    .center(0, -block_h/2)
    .center(*pocket_loc)
    .rect(pocket_w, pocket_h)
    .cutBlind(-pocket_depth)
)

# Final Result
if 'show_object' in globals():
    show_object(result)