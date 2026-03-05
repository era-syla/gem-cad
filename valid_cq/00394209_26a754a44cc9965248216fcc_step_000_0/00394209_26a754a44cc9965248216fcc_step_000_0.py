import cadquery as cq

# -- Parameters --
# Main Box Dimensions
box_width = 45.0
box_depth = 25.0
box_height = 80.0
wall_thickness = 2.0

# Internal Cylinder/Tube Dimensions
tube_od = 16.0
tube_id = 10.0
# Position relative to center of box (shifted to one side)
tube_offset_x = -10.0 

# Top Feature Dimensions
flange_diameter = 32.0
flange_height = 4.0
block_width = 24.0
block_height = 6.0

# Side Hex/Pentagon Feature Dimensions
poly_radius = 7.0 # Circumradius
poly_height = 12.0
poly_sides = 5 # Pentagon as seen in image

# Bottom Spout Dimensions
spout_diameter = 10.0
spout_length = 15.0

# -- Modeling --

# 1. Create the Main Body Box
# Centered on XY plane, sitting on Z=0 initially, then moved up
main_body = (
    cq.Workplane("XY")
    .box(box_width, box_depth, box_height)
    .translate((0, 0, box_height / 2))
)

# 2. Shell the box (create the internal cavity)
# Opening is on the front face (+Y)
# We cut a rectangle slightly smaller than the face, leaving wall thickness
hollow_body = (
    main_body.faces(">Y")
    .workplane()
    .rect(box_width - 2 * wall_thickness, box_height - 2 * wall_thickness)
    .cutBlind(-(box_depth - wall_thickness))
)

# 3. Internal Vertical Column (Tube)
# Cylinder running the full height of the box
internal_column = (
    cq.Workplane("XY")
    .center(tube_offset_x, 0)
    .circle(tube_od / 2)
    .extrude(box_height)
)

# 4. Top Flange (Circular Disk)
# Sits on top of the main body
top_flange = (
    cq.Workplane("XY")
    .workplane(offset=box_height)
    .center(tube_offset_x, 0)
    .circle(flange_diameter / 2)
    .extrude(flange_height)
)

# 5. Top Block (Square Feature)
# Sits on top of the flange
top_block = (
    cq.Workplane("XY")
    .workplane(offset=box_height + flange_height)
    .center(tube_offset_x, 0)
    .rect(block_width, block_width)
    .extrude(block_height)
)

# 6. Pentagonal Prism Feature
# Located at the top corner, opposite the tube side
# Position adjustment: near the back-right corner
poly_x = (box_width / 2) - poly_radius
poly_y = -(box_depth / 2) + poly_radius # aligned near the back wall
poly_feature = (
    cq.Workplane("XY")
    .workplane(offset=box_height)
    .center(poly_x, poly_y)
    .polygon(poly_sides, poly_radius * 2)
    .extrude(poly_height)
)

# 7. Bottom Spout
# Extends downwards from the bottom
bottom_spout = (
    cq.Workplane("XY")
    .center(tube_offset_x, 0)
    .circle(spout_diameter / 2)
    .extrude(-spout_length)
)

# 8. Combine Solids
# Union all parts before cutting the through-hole
solid_geometry = (
    hollow_body
    .union(internal_column)
    .union(top_flange)
    .union(top_block)
    .union(poly_feature)
    .union(bottom_spout)
)

# 9. Create Through-Hole
# Cuts through the spout, body, flange, and block
total_cut_height = spout_length + box_height + flange_height + block_height + 10.0
cut_tool = (
    cq.Workplane("XY")
    .workplane(offset=-spout_length - 5.0)
    .center(tube_offset_x, 0)
    .circle(tube_id / 2)
    .extrude(total_cut_height)
)

# Apply the cut
result = solid_geometry.cut(cut_tool)