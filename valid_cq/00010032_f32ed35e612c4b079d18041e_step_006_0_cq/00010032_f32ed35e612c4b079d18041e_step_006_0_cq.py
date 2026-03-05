import cadquery as cq

def create_vex_c_channel(length_holes, width_holes=5, hole_spacing=0.5, hole_radius=0.091, thickness=0.046):
    """
    Creates a VEX-style C-channel.
    Dimensions are typically in inches for VEX, but units here are generic.
    Standard VEX C-channel is 0.5" hole spacing.
    Width is usually defined by the number of holes (e.g., 2, 3, or 5 holes wide).
    This function approximates the profile.
    
    Args:
        length_holes: Number of holes along the length.
        width_holes: Number of holes along the width (top face). Commonly 2, 3, or 5.
        hole_spacing: Distance between hole centers.
        hole_radius: Radius of the square/circle holes.
        thickness: Material thickness.
    """
    
    # Calculate dimensions
    L = length_holes * hole_spacing
    W = width_holes * hole_spacing
    H = 1.0 * hole_spacing # Flange height is typically 1 unit (0.5")
    
    # Create the base C-profile
    # We will extrude a U-shape
    
    # Outer dimensions
    outer_w = W
    outer_h = H
    
    # Create the profile sketch
    pts = [
        (0, 0),
        (outer_w, 0),
        (outer_w, -outer_h),
        (outer_w - thickness, -outer_h),
        (outer_w - thickness, -thickness),
        (thickness, -thickness),
        (thickness, -outer_h),
        (0, -outer_h),
        (0, 0)
    ]
    
    channel = cq.Workplane("XY").polyline(pts).close().extrude(L)
    
    # Add holes
    # Top face holes (grid)
    # The grid pattern typically has square holes
    
    # Define a custom square hole shape for VEX
    # VEX holes are actually square with rounded corners or just square.
    # Let's use square for simplicity and visual match.
    hole_side = hole_radius * 2 * 0.9 # Slightly smaller than full spacing
    
    # Center the channel along Y for easier hole placement? No, let's keep it as is and shift.
    
    # Create a grid of points for the top face
    x_positions = [thickness + (i + 0.5) * hole_spacing for i in range(width_holes - 1)] 
    # Actually, width holes usually means the width is N * 0.5". The holes are centered in the 0.5" grid.
    # The profile width is W.
    # First hole center is at 0.5 * hole_spacing.
    
    # Top face holes
    top_face_pts = []
    for i in range(length_holes):
        z_pos = (i + 0.5) * hole_spacing
        for j in range(width_holes):
             x_pos = (j + 0.5) * hole_spacing
             top_face_pts.append((x_pos, z_pos))
             
    # Flange holes
    # Left flange (x=0) and Right flange (x=W)
    # Flange is 1 unit high, so 1 row of holes centered.
    flange_height_center = -0.5 * hole_spacing
    
    side_face_pts_left = []
    side_face_pts_right = []
    
    for i in range(length_holes):
        z_pos = (i + 0.5) * hole_spacing
        side_face_pts_left.append((flange_height_center, z_pos))
        side_face_pts_right.append((flange_height_center, z_pos))

    # Cut holes on Top
    # Rotate to align with the extrusion direction (Z) and the face
    channel = channel.faces(">Z").workplane(centerOption="CenterOfBoundBox") \
        .pushPoints(top_face_pts) \
        .rect(hole_side, hole_side) \
        .cutThruAll()
        
    # Cut holes on Sides
    # We need to select faces carefully.
    
    # Workplane orientation is tricky after extrude. 
    # Let's cut relative to the global coordinates.
    
    # Side 1 (Left, near X=0)
    channel = channel.faces("<X").workplane(centerOption="ProjectedOrigin") \
        .pushPoints([(z, y) for y, z in side_face_pts_left]) \
        .rect(hole_side, hole_side) \
        .cutThruAll()
        
    # Side 2 (Right, near X=W)
    channel = channel.faces(">X").workplane(centerOption="ProjectedOrigin") \
        .pushPoints([(z, y) for y, z in side_face_pts_right]) \
        .rect(hole_side, hole_side) \
        .cutThruAll()

    return channel

def create_vex_angle(length_holes, width_holes=1, height_holes=1, hole_spacing=0.5, hole_radius=0.091, thickness=0.046):
    """
    Creates a VEX-style Angle bracket (L-channel).
    """
    L = length_holes * hole_spacing
    W = width_holes * hole_spacing
    H = height_holes * hole_spacing
    
    pts = [
        (0, 0),
        (W, 0),
        (W, -thickness),
        (thickness, -thickness),
        (thickness, -H),
        (0, -H),
        (0, 0)
    ]
    
    angle = cq.Workplane("XY").polyline(pts).close().extrude(L)
    
    hole_side = hole_radius * 2 * 0.9
    
    # Top face holes
    top_face_pts = []
    for i in range(length_holes):
        z_pos = (i + 0.5) * hole_spacing
        for j in range(width_holes):
             x_pos = (j + 0.5) * hole_spacing
             top_face_pts.append((x_pos, z_pos))
             
    # Side face holes
    side_face_pts = []
    for i in range(length_holes):
        z_pos = (i + 0.5) * hole_spacing
        for k in range(height_holes):
             y_pos = -(k + 0.5) * hole_spacing
             side_face_pts.append((y_pos, z_pos))

    # Cut Top
    # We have to be careful with coordinate systems. 
    # The points for top face are in (X, Z) relative to global, where Y=0 is the face.
    # centerOption="ProjectedOrigin" keeps (0,0,0) as reference.
    angle = angle.faces(">Y").workplane(centerOption="ProjectedOrigin") \
        .pushPoints(top_face_pts) \
        .rect(hole_side, hole_side) \
        .cutThruAll()
        
    # Cut Side
    angle = angle.faces("<X").workplane(centerOption="ProjectedOrigin") \
        .pushPoints([(z, y) for y, z in side_face_pts]) \
        .rect(hole_side, hole_side) \
        .cutThruAll()
        
    return angle

# --- Build the Parts ---

# Parameters
hole_spacing = 12.7 # mm (0.5 inch standard)
thickness = 1.2 # mm
hole_r = 4.0 # mm square approx

# Part 1: Top Left - Long C-Channel
# Looks like 1x2x1x35 holes? Let's count approximate holes from image. 
# It looks like a standard 1x2x1 C-channel, about 25-30 holes long.
c1 = create_vex_c_channel(length_holes=25, width_holes=2, hole_spacing=hole_spacing, hole_radius=hole_r/2, thickness=thickness)
c1 = c1.translate((-300, 200, 0))

# Part 2: Top Middle-Left - Short C-Channel
# Looks like 15 holes long.
c2 = create_vex_c_channel(length_holes=15, width_holes=2, hole_spacing=hole_spacing, hole_radius=hole_r/2, thickness=thickness)
c2 = c2.translate((-100, 200, 0))

# Part 3: Top Middle-Right - Short C-Channel
# Looks like 15 holes long.
c3 = create_vex_c_channel(length_holes=15, width_holes=2, hole_spacing=hole_spacing, hole_radius=hole_r/2, thickness=thickness)
c3 = c3.translate((50, 200, 0))

# Part 4: Top Right - Angle Piece
# Looks like 1x1 angle, about 25 holes long.
a1 = create_vex_angle(length_holes=25, width_holes=1, height_holes=1, hole_spacing=hole_spacing, hole_radius=hole_r/2, thickness=thickness)
a1 = a1.translate((200, 200, 0))

# Part 5: The Main Assembly
# It consists of two long C-channels forming a cross/plus shape.
# One is lying flat (wide side horizontal), the other is crossing it.

# Horizontal Beam (in image view)
# Looks like a 5-wide C-channel. Very wide.
# Or maybe two 2-wide channels back to back?
# Let's assume it's a 5-wide channel (standard VEX part).
# Length: ~35 holes.
main_beam_1 = create_vex_c_channel(length_holes=35, width_holes=5, hole_spacing=hole_spacing, hole_radius=hole_r/2, thickness=thickness)
# Rotate and position
main_beam_1 = main_beam_1.rotate((0,0,0), (0,0,1), 90).translate((100, -100, 0))


# Vertical Beam (crossing the first one)
# Looks like a 2-wide C-channel.
# It crosses over the top of the 5-wide one.
# Length: ~35 holes.
main_beam_2 = create_vex_c_channel(length_holes=35, width_holes=2, hole_spacing=hole_spacing, hole_radius=hole_r/2, thickness=thickness)
# Position it to cross. It needs to be higher up Z to clear the flanges or sit inside?
# In the image, they seem to intersect or one sits on top.
# The 2-wide one is running "longitudinally" relative to the view.
# Let's translate it.
# Center of 5-wide beam (width) is at Y = -100 + length/2 approximately? No.
# Let's center everything around origin for the assembly.

# Re-centering strategy for assembly:
mb1_len = 35 * hole_spacing
mb1_wid = 5 * hole_spacing
mb1 = create_vex_c_channel(length_holes=35, width_holes=5, hole_spacing=hole_spacing, hole_radius=hole_r/2, thickness=thickness)
# Center mb1 on origin
mb1 = mb1.translate((-mb1_wid/2, 0, -mb1_len/2)) # Centered on X, Z=0 is start
# Rotate to lie along Y axis
mb1 = mb1.rotate((0,0,0), (1,0,0), -90) # Now length is along Y
# Now it is: Width along X, Flanges pointing down Z (if created that way), Length along Y.
# Let's check create_vex_c_channel orientation:
# Profile in XY, Extruded along Z.
# Profile: width along X, height along -Y.
# So initially: Length along Z, Width along X, Height along -Y.
# We want: Length along X (for the cross bar), Width along Y, Height along Z.

# Assembly Piece 1: The wide cross bar (5 holes wide)
beam_wide = create_vex_c_channel(length_holes=35, width_holes=5, hole_spacing=hole_spacing, hole_radius=hole_r/2, thickness=thickness)
# Rotate so length is along X axis, Flat face is on XY plane (facing up)
# Initial: Z=Length, X=Width, -Y=Height (Flanges down)
# Rotate around Y axis by 90 deg?
# X becomes Z, Z becomes -X. Not quite.
# Rotate around X axis -90 deg -> Y becomes Z, Z becomes -Y (Length along -Y).
# Let's just rotate (0,1,0) 90 degrees.
# Z (Length) -> X. X (Width) -> -Z. Y (Height) -> Y.
# We want Width horizontal.
beam_wide = beam_wide.rotate((0,0,0), (0,1,0), 90) # Length along X, Width along Z (vertical?? No).
# Initial: Width is X.
# We want Width along Y. Length along X. Flanges down (-Z).

beam_wide = create_vex_c_channel(length_holes=35, width_holes=5, hole_spacing=hole_spacing, hole_radius=hole_r/2, thickness=thickness)
# Initial: Length=Z, Width=X, Height=-Y (flanges point to -Y)
# Goal: Length=X, Width=Y, Height=-Z
beam_wide = beam_wide.rotate((0,0,0), (0,0,1), 90) # Length=Z, Width=Y, Height=X (flanges point to +X) 
beam_wide = beam_wide.rotate((0,0,0), (0,1,0), 90) # Length=X, Width=Y, Height=-Z (flanges point to -Z) !! Correct.
# Center it
beam_wide = beam_wide.translate((-35*hole_spacing/2, -5*hole_spacing/2, hole_spacing)) 

# Assembly Piece 2: The narrow longitudinal bar (2 holes wide)
beam_narrow = create_vex_c_channel(length_holes=35, width_holes=2, hole_spacing=hole_spacing, hole_radius=hole_r/2, thickness=thickness)
# Goal: Length=Y, Width=X, Height=-Z.
# Initial: Length=Z, Width=X, Height=-Y.
beam_narrow = beam_narrow.rotate((0,0,0), (1,0,0), -90) # Length=Y, Width=X, Height=Z (flanges point +Z)
# The image shows the narrow beam ON TOP of the wide beam, flanges usually point down or up.
# In the image, the narrow beam looks like flanges are pointing DOWN into the wide beam, or it's inside.
# Let's put flanges pointing down (-Z).
beam_narrow = beam_narrow.rotate((0,0,0), (1,0,0), 180) # Flip Z
# Center it
beam_narrow = beam_narrow.translate((-2*hole_spacing/2, -35*hole_spacing/2, hole_spacing + hole_spacing)) # Sit on top of the other beam height

# There's also a smaller piece perpendicular to the narrow beam in the assembly, looks like an L-bracket or short C-channel connecting them?
# Actually, looking closely at the intersection:
# It looks like the narrow channel passes through or over the wide one.
# There is a vertical piece or a bracket at the junction.
# Let's simplify and just place the two main crossing beams as the "Assembly".

# Combine all objects
result = c1.union(c2).union(c3).union(a1).union(beam_wide).union(beam_narrow)