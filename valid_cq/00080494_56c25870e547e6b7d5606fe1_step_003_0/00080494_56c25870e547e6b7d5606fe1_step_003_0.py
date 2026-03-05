import cadquery as cq

# --- Parameters & Dimensions ---
# Back Row (Plates)
plate_h = 15.0
plate_th = 2.0
plate_small_w = 25.0
plate_long_w = 80.0
plate_gap = 10.0
row_back_y = 60.0

# Chamfered Block
block_l = 50.0
block_w = 30.0
block_h = 12.0
block_chamfer = 8.0

# Rails/Bars
bar_w = 5.0
bar_h = 6.0
bar_len_long = 90.0
bar_len_short = 60.0

# Flat Plate
flat_w = 50.0
flat_h = 30.0
flat_th = 1.5

# --- Geometry Construction ---

# 1. Back Row: Vertical Plates
# Three small plates
p1 = cq.Workplane("XY").box(plate_small_w, plate_th, plate_h)\
    .translate((-85, row_back_y, plate_h/2))
p2 = cq.Workplane("XY").box(plate_small_w, plate_th, plate_h)\
    .translate((-55, row_back_y, plate_h/2))
p3 = cq.Workplane("XY").box(plate_small_w, plate_th, plate_h)\
    .translate((-25, row_back_y, plate_h/2))

# Long plate
p4 = cq.Workplane("XY").box(plate_long_w, plate_th, plate_h)\
    .translate((35, row_back_y, plate_h/2))

# End flat strip
p5 = cq.Workplane("XY").box(25, 10, 1.5)\
    .translate((95, row_back_y, 0.75))

# 2. Chamfered Block (Front Left)
base_block = cq.Workplane("XY").box(block_l, block_w, block_h)\
    .translate((-70, 20, block_h/2))
# Apply chamfer to vertical edges
base_block = base_block.edges("|Z").chamfer(block_chamfer)

# 3. Bar Assembly (Front Center)
# Long bar with angled cut (Ramp)
bar_long = cq.Workplane("XY").box(bar_len_long, bar_w, bar_h)\
    .translate((0, 25, bar_h/2))

# Create a cutting tool for the sloped tip
# Profile in XZ plane: triangle to remove top-left corner
cut_pts = [
    (-bar_len_long/2, 0),
    (-bar_len_long/2, bar_h + 0.1),
    (-bar_len_long/2 + 20, bar_h + 0.1)
]
cutter = cq.Workplane("XZ").polyline(cut_pts).close().extrude(20)\
    .translate((0, 15, 0)) # Position in Y to intersect the bar

bar_long = bar_long.cut(cutter)

# Short straight bars
bar_short1 = cq.Workplane("XY").box(bar_len_short, bar_w, bar_h)\
    .translate((-15, 17, bar_h/2))
bar_short2 = cq.Workplane("XY").box(bar_len_short, bar_w, bar_h)\
    .translate((-15, 9, bar_h/2))

# Perpendicular spacer block
bar_spacer = cq.Workplane("XY").box(6, 22, 6)\
    .translate((20, 17, 3))

# 4. Plate with Holes (Front Right)
plate_main = cq.Workplane("XY").box(flat_w, flat_h, flat_th)\
    .translate((60, 15, flat_th/2))
# Cut holes
plate_main = plate_main.faces(">Z").workplane()\
    .pushPoints([(10, -5), (18, -8)]).circle(3.5).cutThruAll()

# 5. Small Miscellaneous Parts
small_cube = cq.Workplane("XY").box(6, 6, 6)\
    .translate((65, -5, 3))
small_tab = cq.Workplane("XY").box(2, 10, 15)\
    .translate((80, -5, 7.5))

# --- Assembly ---
# Union all parts into a single result
result = p1.union(p2).union(p3).union(p4).union(p5)\
           .union(base_block)\
           .union(bar_long).union(bar_short1).union(bar_short2).union(bar_spacer)\
           .union(plate_main).union(small_cube).union(small_tab)