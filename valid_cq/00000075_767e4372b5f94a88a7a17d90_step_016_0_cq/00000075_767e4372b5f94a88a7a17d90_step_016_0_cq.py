import cadquery as cq

# Parameters for dimensions
table_width = 1000.0  # Overall width of the table
table_depth = 400.0   # Overall depth of the table
table_height = 800.0  # Overall height of the table

leg_width = 40.0      # Width of the square legs
top_thickness = 25.0  # Thickness of the table top
apron_height = 80.0   # Height of the skirt/apron under the top
shelf_height = 500.0  # Height from floor to top of shelf
shelf_thickness = 15.0 # Thickness of the shelf

# Derived parameters
leg_x_offset = table_width / 2 - leg_width / 2
leg_y_offset = table_depth / 2 - leg_width / 2
apron_thickness = 20.0 # Assumed thickness for the apron pieces

# 1. Create the Table Top
top = cq.Workplane("XY").box(table_width, table_depth, top_thickness) \
    .translate((0, 0, table_height - top_thickness / 2))

# 2. Create the Legs
# Front Left Leg
leg_fl = cq.Workplane("XY").box(leg_width, leg_width, table_height - top_thickness) \
    .translate((-leg_x_offset, -leg_y_offset, (table_height - top_thickness) / 2))

# Front Right Leg
leg_fr = cq.Workplane("XY").box(leg_width, leg_width, table_height - top_thickness) \
    .translate((leg_x_offset, -leg_y_offset, (table_height - top_thickness) / 2))

# Back Left Leg
leg_bl = cq.Workplane("XY").box(leg_width, leg_width, table_height - top_thickness) \
    .translate((-leg_x_offset, leg_y_offset, (table_height - top_thickness) / 2))

# Back Right Leg
leg_br = cq.Workplane("XY").box(leg_width, leg_width, table_height - top_thickness) \
    .translate((leg_x_offset, leg_y_offset, (table_height - top_thickness) / 2))


# 3. Create the Apron (Skirt)
# This sits just under the top, connecting the legs
apron_w_length = table_width - 2 * leg_width
apron_d_length = table_depth - 2 * leg_width
apron_z_center = table_height - top_thickness - apron_height / 2

# Front Apron
apron_front = cq.Workplane("XY").box(apron_w_length, apron_thickness, apron_height) \
    .translate((0, -leg_y_offset + (leg_width - apron_thickness)/2, apron_z_center))

# Back Apron
apron_back = cq.Workplane("XY").box(apron_w_length, apron_thickness, apron_height) \
    .translate((0, leg_y_offset - (leg_width - apron_thickness)/2, apron_z_center))

# Left Side Apron
apron_left = cq.Workplane("XY").box(apron_thickness, apron_d_length, apron_height) \
    .translate((-leg_x_offset + (leg_width - apron_thickness)/2, 0, apron_z_center))

# Right Side Apron
apron_right = cq.Workplane("XY").box(apron_thickness, apron_d_length, apron_height) \
    .translate((leg_x_offset - (leg_width - apron_thickness)/2, 0, apron_z_center))


# 4. Create the Shelf and Divider
# The shelf appears to span the full width between legs and full depth
shelf_z_center = shelf_height - shelf_thickness / 2

shelf = cq.Workplane("XY").box(apron_w_length, table_depth, shelf_thickness) \
    .translate((0, 0, shelf_z_center))

# The vertical divider under the top, connecting to the shelf
# It is centered and has a specific width/depth. Looks like it splits the open space.
divider_height = (table_height - top_thickness) - shelf_height
divider = cq.Workplane("XY").box(apron_thickness, table_depth, divider_height) \
    .translate((0, 0, shelf_height + divider_height / 2))


# 5. Combine all parts
result = top.union(leg_fl).union(leg_fr).union(leg_bl).union(leg_br) \
            .union(apron_front).union(apron_back).union(apron_left).union(apron_right) \
            .union(shelf).union(divider)

# Optional: Subtract the volume where the legs intersect the shelf/aprons 
# if you wanted a pure assembly, but union creates a single solid as requested.