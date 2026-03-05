import cadquery as cq

# --- Parametric Dimensions ---
# Main body parameters
hole_count_x = 5  # Number of main holes in the long direction
hole_count_y = 2  # Number of main holes in the short direction
hole_dia = 18.5   # Diameter of the main holes (typical for 18650s is 18mm + tolerance)
wall_thickness = 1.5 # Thickness of the walls between holes
cell_spacing_x = hole_dia + wall_thickness # Center-to-center distance
cell_spacing_y = hole_dia * 0.866 + wall_thickness # Hexagonal packing vertical spacing approximation, but looks rectangular in image. Let's assume close rectangular or slightly shifted.
# Looking closely at the image, the packing is staggered (hexagonal).
# Row 2 is shifted relative to Row 1.
is_staggered = True

# Main height
plate_height = 8.0

# Clip/Tab parameters
tab_width = 8.0
tab_length = 6.0
tab_height = plate_height
clip_post_dia = 3.5
clip_post_height = 4.0
clip_slot_width = 1.0

# Side feature (the weird L-shape protrusion)
side_feature_dia = 12.0
side_feature_offset = cell_spacing_x / 2.0

# --- Helper Calculations ---
outer_radius = (hole_dia / 2.0) + wall_thickness
offset_x = cell_spacing_x
offset_y = cell_spacing_y if not is_staggered else (outer_radius * 2 * 0.866) # Hex spacing height

# --- Building the Geometry ---

# 1. Create the base cells (Cylinders)
# We will create a list of center points for the cylinders.
points = []

# Row 1 (Bottom in image perspective, 5 items)
for i in range(hole_count_x):
    x = i * offset_x
    y = 0
    points.append((x, y))

# Row 2 (Top in image perspective, 5 items, shifted)
# Looking at the image, the top row is shifted to the right by half a pitch
shift_x = offset_x / 2.0
for i in range(hole_count_x):
    x = (i * offset_x) + shift_x
    y = offset_y
    points.append((x, y))

# Create the main cylinders fused together
base_sk = cq.Sketch().push(points).circle(outer_radius)
base_solid = cq.Workplane("XY").placeSketch(base_sk).extrude(plate_height)

# Create the holes
holes_sk = cq.Sketch().push(points).circle(hole_dia / 2.0)
body = base_solid.cut(cq.Workplane("XY").placeSketch(holes_sk).extrude(plate_height))


# 2. Add the Side Tabs/Clips
# There are tabs on the corners. Let's identify the attachment points.
# Bottom-left: near point (0,0)
# Bottom-right: near point ((N-1)*offset, 0)
# Top-left: near point (shift, offset_y)
# Top-right: near point ((N-1)*offset + shift, offset_y)

# From the image:
# - One tab on the bottom-right cylinder.
# - One tab on the top-right cylinder.
# - One tab on the top-left cylinder.
# - The bottom-left has the special circular feature.

# Let's define a function to make a standard clip tab
def make_clip_tab(loc_point, direction_vec):
    # Base block of the tab
    # direction_vec should be roughly normal to the cylinder surface
    
    # Position relative to the cylinder center
    center_dist = outer_radius + (tab_length / 2.0) - 1.0 # -1 for overlap
    
    # Calculate global position
    pos_x = loc_point[0] + direction_vec[0] * center_dist
    pos_y = loc_point[1] + direction_vec[1] * center_dist
    
    # Create the rectangular base
    # We rotate the box to align with the angle
    angle = 0 # Simplified: assume axis aligned for this specific geometry
    if direction_vec[1] > 0.5: angle = 90
    elif direction_vec[1] < -0.5: angle = -90
    
    tab_base = (cq.Workplane("XY")
                .center(pos_x, pos_y)
                .box(tab_length, tab_width, tab_height)
                )
    
    # Add the post on top
    # The post is hollow with a slot
    post_center = (pos_x + (direction_vec[0] * tab_length/4), pos_y + (direction_vec[1] * tab_length/4))
    
    post = (cq.Workplane("XY")
            .center(post_center[0], post_center[1])
            .workplane(offset=plate_height)
            .circle(clip_post_dia/2.0)
            .extrude(clip_post_height)
           )
    
    # Cut the inside of the post
    post_hole = (cq.Workplane("XY")
            .center(post_center[0], post_center[1])
            .workplane(offset=plate_height)
            .circle((clip_post_dia/2.0) - 0.8)
            .extrude(clip_post_height)
           )
    
    # Cut the slot in the post
    slot = (cq.Workplane("XY")
            .center(post_center[0], post_center[1])
            .workplane(offset=plate_height)
            .rect(clip_post_dia + 2, clip_slot_width)
            .extrude(clip_post_height)
           )
    
    return tab_base.union(post).cut(post_hole).cut(slot)

# Apply tabs based on the image locations
# Bottom-Right (Last on Row 1)
pt_br = points[hole_count_x - 1]
tab1 = make_clip_tab(pt_br, (1, 0)) # Pointing Right

# Top-Right (Last on Row 2)
pt_tr = points[-1]
tab2 = make_clip_tab(pt_tr, (1, 0)) # Pointing Right

# Top-Left (First on Row 2)
pt_tl = points[hole_count_x]
tab3 = make_clip_tab(pt_tl, (-1, 0)) # Pointing Left

# Fuse tabs to body
body = body.union(tab1).union(tab2).union(tab3)

# 3. Add the special side feature (Bottom-Left)
# This looks like an extra half-cylinder attached to the side with an L-shape rib on top
pt_bl = points[0]
feature_center = (pt_bl[0] - offset_x * 0.5, pt_bl[1] + offset_y * 0.3)

# Create the extra circular pad
extra_pad = (cq.Workplane("XY")
             .center(feature_center[0], feature_center[1])
             .circle(outer_radius)
             .extrude(plate_height/2.0) # It looks thinner than the main body in the image
            )

# Create the L-shape rib
# Define L-shape path
l_rib_width = 1.5
l_rib_height = plate_height
l_rib = (cq.Workplane("XY")
         .center(feature_center[0], feature_center[1])
         .rect(outer_radius, l_rib_width) # Horizontal part
         .extrude(l_rib_height)
         )
l_rib2 = (cq.Workplane("XY")
         .center(feature_center[0] + outer_radius/2 - l_rib_width/2, feature_center[1] + outer_radius/2 - l_rib_width/2)
         .rect(l_rib_width, outer_radius) # Vertical part
         .extrude(l_rib_height)
         )

body = body.union(extra_pad).union(l_rib).union(l_rib2)

# 4. Final Clean-up and Fillets (Optional, to make it look molded)
# Fillet the edges where cylinders meet to smooth it out like the image
# This is computationally expensive, so often skipped in basic parametric scripts, 
# but we can try a small fillet on vertical edges.
try:
    result = body.edges("|Z").fillet(0.5)
except:
    result = body

# Ensure the result variable is set
result = result