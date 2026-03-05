import cadquery as cq

# Parameters for dimensions
width = 54.0
length = 90.0
thickness = 8.0
main_fillet_radius = 6.0
edge_soften_radius = 1.0

# Battery cover parameters
cover_width = 24.0
cover_length = 42.0
cover_offset_y = -10.0
cover_depth = 0.3

# Switch parameters
switch_offset_y = 26.0
switch_w = 11.0
switch_h = 16.0
switch_thick = 1.2
switch_slider_h = 4.0

# Button parameters
btn_offset_x = -17.0
btn_offset_y = -34.0
btn_size = 7.0
btn_height = 0.8
btn_corner_radius = 2.2

# 1. Create the Main Body
# A rounded box with softened edges
main_body = (
    cq.Workplane("XY")
    .box(width, length, thickness)
    .edges("|Z")
    .fillet(main_fillet_radius)
    .edges("#Z")  # Select edges on top and bottom faces
    .fillet(edge_soften_radius)
)

# 2. Add Battery Cover Indentation
# Select the top face and cut a shallow rectangle
main_body = (
    main_body.faces(">Z")
    .workplane()
    .center(0, cover_offset_y)
    .rect(cover_width, cover_length)
    .cutBlind(-cover_depth)
)

# 3. Create the Switch Assembly (Housing + Slider)
# Construct separately and union to avoid selection complexity
switch_housing = (
    cq.Workplane("XY")
    .rect(switch_w, switch_h)
    .extrude(switch_thick)
    .edges("|Z")
    .fillet(0.3) # Micro fillet on housing corners
)

# Cut the pocket inside the housing
switch_housing = (
    switch_housing.faces(">Z")
    .workplane()
    .rect(switch_w - 3.0, switch_h - 3.0)
    .cutBlind(-0.7)
)

# Create the slider nub
slider = (
    cq.Workplane("XY")
    .rect(switch_w - 5.0, 5.0)
    .extrude(switch_thick) # Same height as housing top roughly
    .edges("|Z")
    .fillet(0.5)
    .translate((0, -2.5, 0)) # Shift slider position inside housing
)

# Combine switch parts and position on main body
switch_assy = switch_housing.union(slider)
switch_assy = switch_assy.translate((0, switch_offset_y, thickness / 2))

# 4. Create the Bottom Button
# Rounded square button
button = (
    cq.Workplane("XY")
    .box(btn_size, btn_size, btn_height)
    .edges("|Z")
    .fillet(btn_corner_radius)
    .faces(">Z")
    .edges()
    .fillet(0.4) # Soften top edge
    .translate((btn_offset_x, btn_offset_y, thickness / 2 + btn_height / 2))
)

# 5. Final Assembly
result = main_body.union(switch_assy).union(button)