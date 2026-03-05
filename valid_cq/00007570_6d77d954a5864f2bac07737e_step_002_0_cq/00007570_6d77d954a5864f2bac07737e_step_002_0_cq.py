import cadquery as cq

# --- Parametric Dimensions ---
# Overall dimensions
width = 60.0    # Overall width of the part
height = 80.0   # Overall height of the part
thickness = 20.0 # Thickness of the main block

# Center Bore dimensions
bore_diameter = 25.0
chamfer_outer_diameter = 35.0 # The wider opening of the chamfer
chamfer_depth = 3.0           # Approximate depth of the countersink/chamfer

# Top features
top_v_depth = 15.0       # How deep the V/U cut goes from the top edge
top_land_width = 12.0    # Width of the flat area on top sides

# Top holes
top_hole_diameter = 6.0
top_hole_depth = 15.0    # Blind hole depth

# Bottom features
bottom_cutout_height = 3.0
bottom_cutout_width = 40.0

# --- Modeling Strategy ---
# 1. Start with a basic rectangular block.
# 2. Cut the U/V shape from the top.
# 3. Cut the relief from the bottom.
# 4. Create the main center bore.
# 5. Add the chamfer/countersink to the center bore.
# 6. Drill the top mounting holes.

# --- Geometry Generation ---

# 1. Base Block
# We center the part on X and Z for symmetry, but align Y (thickness) to make sketching easier.
result = cq.Workplane("XY").box(width, height, thickness)

# 2. Cut the top "Saddle" shape
# We'll create a profile on the front face to cut away the material.
# Calculating the points for the top cut
# We need an arc or a spline connecting the two flat lands. 
# Looking at the image, it looks like two angled lines connecting to a central fillet or a tangent arc.
# Let's simplify as a large radius arc cut.

# Determine the radius of the top cut
# The cut width is width - 2*top_land_width
cut_width = width - 2 * top_land_width
# A 3-point arc needs a radius calculation or just use the logic of the cut.
# Let's use a cutting tool approach on the XZ plane (front view equivalent).

# Re-orienting thinking: It's easier to sketch the profile of the front face and extrude.
# Let's restart the workflow for a cleaner parametric build.

# --- Revised Geometry Generation ---

# Create the main profile on the XY plane (Front View)
# We will draw the entire outer contour then extrude.

def create_main_body():
    # Points definition
    x_half = width / 2.0
    y_top = height / 2.0
    y_bottom = -height / 2.0
    
    # Top cut calculations
    # The cut starts at x = +/- (width/2 - top_land_width)
    # The cut bottom is at y = y_top - top_v_depth
    
    p_tl = (-x_half, y_top) # Top Left
    p_tr = (x_half, y_top)  # Top Right
    p_bl = (-x_half, y_bottom) # Bottom Left
    p_br = (x_half, y_bottom)  # Bottom Right
    
    # Top cut start points
    p_cut_start_l = (-x_half + top_land_width, y_top)
    p_cut_start_r = (x_half - top_land_width, y_top)
    p_cut_bottom = (0, y_top - top_v_depth)
    
    # Bottom cutout points
    p_bot_cut_l = (-bottom_cutout_width/2, y_bottom)
    p_bot_cut_r = (bottom_cutout_width/2, y_bottom)
    p_bot_cut_l_top = (-bottom_cutout_width/2, y_bottom + bottom_cutout_height)
    p_bot_cut_r_top = (bottom_cutout_width/2, y_bottom + bottom_cutout_height)

    sketch = (
        cq.Workplane("XY")
        .moveTo(p_bl[0], p_bl[1])
        .lineTo(p_bot_cut_l[0], p_bot_cut_l[1])
        .lineTo(p_bot_cut_l_top[0], p_bot_cut_l_top[1])
        .lineTo(p_bot_cut_r_top[0], p_bot_cut_r_top[1])
        .lineTo(p_bot_cut_r[0], p_bot_cut_r[1])
        .lineTo(p_br[0], p_br[1])
        .lineTo(p_tr[0], p_tr[1])
        .lineTo(p_cut_start_r[0], p_cut_start_r[1])
        # Create a tangent arc or spline for the top dip
        .threePointArc(p_cut_bottom, p_cut_start_l)
        .lineTo(p_tl[0], p_tl[1])
        .close()
    )
    
    return sketch.extrude(thickness)

result = create_main_body()

# 3. Main Center Bore
result = (
    result.faces(">Z") # Select front face
    .workplane()
    .center(0, 0)      # Ensure we are at center
    .hole(bore_diameter)
)

# 4. Countersink / Chamfer on the Bore
# The image shows a specific smooth countersink or large chamfer.
# We will select the edge of the hole on the front face.
# Note: Since we extruded in +Z, the front face is >Z. The hole goes through.
# We need to select the circular edge on the front face.

result = (
    result.faces(">Z")
    .edges(cq.selectors.RadiusNthSelector(0)) # Select the inner hole edge
    .chamfer((chamfer_outer_diameter - bore_diameter) / 2)
)

# 5. Top Mounting Holes
# These are vertical holes on the flat "lands" on top.
# We need to locate their centers.

hole_x_offset = (width/2) - (top_land_width/2) 

result = (
    result.faces(">Y") # Select the top-most faces
    .workplane()
    .pushPoints([(-hole_x_offset, 0), (hole_x_offset, 0)]) # X offset, Z center (local Y)
    .hole(top_hole_diameter, top_hole_depth)
)

# Apply a small fillet to the bottom cutout edges for visual accuracy if desired,
# though the image looks fairly sharp there. The top saddle looks smooth.
# The image shows a fillet at the bottom of the top 'V'. 
# Since we used threePointArc, it is already smooth.

# Optional: Fillet the vertical edges slightly if needed, but the image shows sharp edges.
# The main bore chamfer in the image looks slightly rounded (like a fillet) rather than a straight chamfer,
# but a chamfer is standard for countersinks. If a fillet is required instead:
# result = result.faces(">Z").edges(cq.selectors.RadiusNthSelector(0)).fillet(2.0)
# But we will stick with the chamfer based on typical mechanical design.