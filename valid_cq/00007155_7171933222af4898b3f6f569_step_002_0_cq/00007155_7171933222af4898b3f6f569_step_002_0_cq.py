import cadquery as cq

# --- Parametric Variables ---
# Main enclosure dimensions
encl_outer_dia = 50.0
encl_height = 20.0
wall_thickness = 2.0
floor_thickness = 2.0

# Inner mounting post dimensions
post_dia = 3.0
post_height = 15.0

# Port cutout dimensions
port_width = 12.0
port_height = 6.0
port_depth = 4.0 # How much it protrudes into the inner volume

# Dimensions for the separate floating blocks (approximated from image)
# These appear to be batteries or other internal components placed nearby
block_large_w = 30.0
block_large_d = 20.0
block_large_h = 10.0

block_med_w = 20.0
block_med_d = 20.0
block_med_h = 8.0

block_small_w = 15.0
block_small_d = 10.0
block_small_h = 8.0

puck_dia = 12.0
puck_height = 8.0

# Spacing factor for arranging the floating items
spacing = 10.0

# --- Geometry Construction ---

# 1. Main Circular Enclosure
# Create the base cylinder
enclosure = cq.Workplane("XY").circle(encl_outer_dia / 2.0).extrude(encl_height)

# Create the hollow interior (shell)
# We select the top face and shell it inwards.
# Note: shelling with a positive value adds material, negative removes. 
# Alternatively, we can cut a smaller cylinder. Let's cut for precision control.
inner_cut = (
    cq.Workplane("XY")
    .workplane(offset=floor_thickness)
    .circle((encl_outer_dia / 2.0) - wall_thickness)
    .extrude(encl_height - floor_thickness)
)
enclosure = enclosure.cut(inner_cut)

# 2. Interior Features
# Add a mounting post (cylinder) inside
post = (
    cq.Workplane("XY")
    .workplane(offset=floor_thickness)
    .center(-encl_outer_dia/4, 0)
    .circle(post_dia / 2.0)
    .extrude(post_height)
)
enclosure = enclosure.union(post)

# Add a "port" housing block on the inner wall
# This looks like a rectangular protrusion from the inner wall for a connector
port_housing = (
    cq.Workplane("XY")
    .workplane(offset=encl_height - port_height - 2.0) # Positioned near top
    .center(encl_outer_dia/2.0 - wall_thickness - 1.0, 0) # Near edge
    .box(5, port_width + 4, port_height) # Slightly larger than cut
)

# Add a cutout to the port housing to make it look like a connector
port_cutout = (
    cq.Workplane("XY")
    .workplane(offset=encl_height - port_height - 2.0 + 1) 
    .center(encl_outer_dia/2.0 - wall_thickness - 1.0, 0)
    .box(6, port_width, port_height - 2) 
)
port_feature = port_housing.cut(port_cutout)
enclosure = enclosure.union(port_feature)


# 3. Create the external floating components
# To match the image layout, we'll create separate solids and translate them.

# Large Block (Top right in cluster)
block1 = cq.Workplane("XY").box(block_large_w, block_large_d, block_large_h)
block1 = block1.translate((40, 40, block_large_h/2))

# Medium Block 1 (Top left in cluster)
block2 = cq.Workplane("XY").box(block_med_w, block_med_d, block_med_h)
block2 = block2.translate((0, 50, block_med_h/2))

# Medium Block 2 (Bottom right in cluster)
block3 = cq.Workplane("XY").box(block_med_w, block_med_d, block_med_h)
block3 = block3.translate((40, 10, block_med_h/2))

# Small rectangular block (Bottom left in cluster)
block4 = cq.Workplane("XY").box(block_large_w, block_large_d/1.5, block_large_h*0.8) # Adjusted to match aspect ratio
block4 = block4.translate((-10, 25, (block_large_h*0.8)/2))

# Small Puck/Cylinder (Far right)
puck = cq.Workplane("XY").circle(puck_dia/2).extrude(puck_height)
puck = puck.translate((60, -10, 0))


# 4. Combine all into one result
# Since CadQuery usually expects a single object for "result" if visualizing, 
# or we just iterate. We will union them all into one disjoint solid for display.
result = enclosure.union(block1).union(block2).union(block3).union(block4).union(puck)

# If you prefer them as an assembly, typically you'd export them separately,
# but 'result' as a union of disjoint bodies works for viewing.