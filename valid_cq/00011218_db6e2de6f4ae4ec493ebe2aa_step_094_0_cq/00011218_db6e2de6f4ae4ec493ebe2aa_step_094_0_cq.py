import cadquery as cq

# Parametric dimensions
length = 100.0         # Total length of the profile
height = 30.0          # Overall height of the main vertical face
top_width = 35.0       # Width of the top flat section
thickness = 1.5        # Thickness of the material
chamfer_size = 5.0     # Size of the angled chamfer
bottom_lip_width = 5.0 # Width of the small bottom lip
back_lip_height = 5.0  # Height of the small back lip

# Notch dimensions (at the start of the profile)
notch_width = 4.0
notch_depth = 5.0
notch_pos_x = 5.0      # Distance from the edge

# Create the profile sketch
# We will draw the cross-section on the YZ plane and extrude along X.
# The profile looks like a modified Z or C channel.
# Starting from bottom-front lip, going up, angled in, flat top, down back.

def create_profile(h, w_top, thk, ch_s, lip_w, back_h):
    # Calculate key coordinate points relative to a local origin (bottom-left corner of main vertical face)
    
    # Outer profile points
    p1 = (0, 0) # Bottom of main vertical face
    p2 = (lip_w, 0) # Tip of bottom lip
    p3 = (lip_w, thk) # Top of bottom lip
    p4 = (thk, thk) # Inner corner of bottom lip
    
    # Calculate main vertical wall inner height
    inner_wall_h = h - thk - ch_s
    
    # We'll construct this by drawing the centerline or outer line and thickening, 
    # but drawing the full loop is more explicit for this shape.
    
    # Let's trace the outer boundary first
    pts = []
    pts.append((0, 0)) # Bottom-left corner of vertical face
    pts.append((lip_w, 0)) # End of bottom lip
    pts.append((lip_w, thk)) # Top of bottom lip
    pts.append((thk, thk)) # Inner corner
    
    # Up the inside of the vertical wall
    # We need the y-coord where the chamfer starts. 
    # Chamfer creates a horizontal offset and vertical offset.
    # Let's assume 45 degree chamfer for simplicity unless specified.
    chamfer_start_y = h - ch_s 
    
    pts.append((thk, chamfer_start_y - thk)) # Top of vertical inner wall
    
    # Angled section (inner)
    # The top width includes the chamfer horizontal component? Let's assume w_top is total width.
    # The chamfer goes Inward.
    
    # Let's restart and draw the OUTER profile to make dimensions clearer.
    # Origin at bottom-left corner of the main vertical face.
    
    # 1. Bottom Lip
    outer_pts = []
    outer_pts.append((lip_w, 0))
    outer_pts.append((0, 0))
    
    # 2. Main Vertical Face
    outer_pts.append((0, h - ch_s))
    
    # 3. Angled Chamfer Face
    # Goes from (0, h-ch_s) to (ch_s, h) assuming 45 deg
    # Looking at image, the chamfer connects vertical face to top face.
    chamfer_dx = ch_s # Horizontal run of chamfer
    chamfer_dy = ch_s # Vertical rise of chamfer
    outer_pts.append((chamfer_dx, h))
    
    # 4. Top Flat Face
    # Total width at top is w_top.
    # The chamfer takes up some width.
    # The previous point is at x = chamfer_dx.
    # The end of the top face is at x = w_top.
    outer_pts.append((w_top, h))
    
    # 5. Back Lip (downwards)
    outer_pts.append((w_top, h - back_h))
    
    # Now trace the INNER profile to close the shape with constant thickness
    # 5_inner
    outer_pts.append((w_top - thk, h - back_h))
    outer_pts.append((w_top - thk, h - thk))
    
    # 4_inner (Top flat face inner)
    # Point before chamfer starts on the inside
    # Chamfer inner start: x = chamfer_dx + something?
    # Actually simpler: offset the lines. 
    # Inner corner between top and chamfer:
    # Outer corner was (chamfer_dx, h). Normal is (-1, 1).
    # This is tricky with raw points. Let's use polyline and offset if possible, 
    # or just calculate specific points for this relatively simple geometry.
    
    # Let's calculate the specific inner knee point for the chamfer
    # Outer line: (0, h-ch_s) -> (ch_s, h)
    # Slope is 1. Shift by thickness perpendicular.
    # Shift vector: (thk/sqrt(2), -thk/sqrt(2)) roughly.
    # But let's look at the image. It's sheet metal.
    # Vertical inner wall ends at y = h - ch_s - (thk correction).
    
    # Let's simplify: 
    # Inner point corresponding to (ch_s, h) is (ch_s + shift, h - thk).
    # Inner point corresponding to (0, h-ch_s) is (thk, h - ch_s - shift).
    
    # Let's just define the inner points manually assuming geometric consistency
    p_top_inner_start = (w_top - thk, h - thk) # Start of top inner flat
    
    # We need the intersection of lines parallel to outer faces.
    # Line 1 (Top): y = h - thk
    # Line 2 (Chamfer): Parallel to y = x + (h - ch_s). 
    #   Outer line goes through (0, h-ch_s) and (ch_s, h). Slope 1.
    #   Equation: y - h = 1 * (x - ch_s) => y = x + h - ch_s.
    #   Inner line is shifted by thickness 'thk'.
    #   Shift perpendicular distance is thk. Vertical shift is thk * sqrt(2).
    #   Equation inner: y = x + h - ch_s - thk * sqrt(2).
    # Line 3 (Vertical): x = thk
    
    import math
    sqrt2 = math.sqrt(2)
    
    # Intersection Top Inner and Chamfer Inner
    # h - thk = x + h - ch_s - thk*sqrt2
    # -thk = x - ch_s - thk*sqrt2
    # x = ch_s + thk*sqrt2 - thk
    ix1 = ch_s + thk * (sqrt2 - 1)
    iy1 = h - thk
    
    # Intersection Chamfer Inner and Vertical Inner
    # y = thk + h - ch_s - thk*sqrt2
    ix2 = thk
    iy2 = h - ch_s + thk * (1 - sqrt2)
    
    outer_pts.append((ix1, iy1))
    outer_pts.append((ix2, iy2))
    outer_pts.append((thk, thk)) # Bottom inner corner
    outer_pts.append((lip_w, thk)) # Top of lip
    
    # Close shape
    outer_pts.append((lip_w, 0))
    
    return outer_pts

# Generate profile points
pts = create_profile(height, top_width, thickness, chamfer_size, bottom_lip_width, back_lip_height)

# Create the extrusion
base = (
    cq.Workplane("YZ")
    .polyline(pts)
    .close()
    .extrude(length)
)

# Add the notch cut
# The notch is on the top edge, near the start.
# Looking at the image, there is a rectangular cutout on the top-back edge.

notch = (
    cq.Workplane("XY")
    .workplane(offset=height) # Move to top plane
    .center(0, 0)
    # Positioning relative to the extrusion center is default, let's use absolute relative to origin
)

# Alternative cutting strategy: Box cut
# The extrusion runs along +X. The profile is on YZ.
# Top face is at Z = height (approx).
# We need to cut into the back edge (positive Y in our profile coordinates).
# Wait, let's check profile coordinates.
# (0,0) is bottom-front. Top-back is (w_top, h).
# So in global coords: Y is "width/depth", Z is "height".
# Extrusion is along X.

# The notch is located at X = notch_pos_x, on the top face (Y near w_top).
notch_cutter = (
    cq.Workplane("XY")
    .workplane(offset=height) # Top of part
    .moveTo(length - notch_pos_x - notch_width/2, top_width) # Position at the back edge
    .rect(notch_width, notch_depth * 2) # Create a rectangle to cut
    .extrude(-thickness * 2) # Cut downwards
)

# Apply the cut.
# Note: The moveTo calculation depends on extrusion direction.
# Workplane("YZ").extrude(length) creates solid from Z=0 to Z=length? No, usually centered=False means 0 to length.
# The profile (0,0) is at global (0,0,0).
# Extrusion goes from X=0 to X=length.
# The notch is at the "start" (left side of image). Let's assume that is near X=0.
# The notch is on the back edge (the lip side). In our profile, that is Y=w_top.

notch_cutter_2 = (
    cq.Workplane("XY")
    .workplane(offset=height)
    .moveTo(notch_pos_x + notch_width/2, top_width) # Near X=0
    .rect(notch_width, notch_depth * 2) # Depth*2 to ensure it cuts through the edge
    .extrude(-10) # Cut down enough
)

# Add the small tab/protrusion on the vertical face if visible
# Looking at the image, there's a small tab sticking out of the vertical face on the left side (start).
tab_height = 2.0
tab_width = 3.0
tab_pos_z = height / 2

tab_cutter = (
    cq.Workplane("YZ")
    .workplane(offset=-1) # Slightly before the start
    .moveTo(0, tab_pos_z)
    .rect(10, tab_height) # Cut a notch into the side?
    # Actually image shows a tab sticking OUT, or is it a slot?
    # It looks like a small tab sticking out from the side face edge.
    # Since we extruded, adding material is easier.
)

# Let's refined the notch based on the image.
# There is a cutout on the top flange.
result = base.cut(notch_cutter_2)

# There is also a small feature on the vertical edge.
# It looks like a small rectangular tab protruding from the end face (X=0)
# on the vertical wall.
tab = (
    cq.Workplane("YZ")
    .moveTo(0, height/2) # Middle of vertical face
    .rect(thickness, 4.0, centered=True) # width, height
    .extrude(-2.0) # Extrude outwards (negative X)
)

# In CadQuery, unions need aligned faces or solids.
# The tab is centered at Y=0 (bottom-left of profile).
# We need to move it to the correct Y and Z.
# Profile Vertical face is at Y=0 (relative to profile start), but extends upwards.
# Actually, our profile starts at (0,0). Vertical face is from (0,0) to (0, h-ch).
# So X=0 (global) is the face. The tab sticks out in -X direction.
# The tab needs to be aligned with the vertical wall.
# Vertical wall is at local Y=0 to Y=thickness.
# Let's align the tab properly.

tab_geo = (
    cq.Workplane("YZ")
    .workplane(offset=0)
    .moveTo(thickness/2, height/2) # Center of the vertical wall thickness, mid-height
    .rect(thickness, 6.0) # Same thickness as wall, 6mm tall
    .extrude(-3.0) # Stick out 3mm
)

result = result.union(tab_geo)

# Refine the notch. The image shows a U-shaped slot.
# My cutter was a rectangle cutting the edge. That works.

# Final cleanup of the variable
result = result