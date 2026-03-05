import cadquery as cq

# Parameters
width = 60.0       # Total width (X-direction)
height = 60.0      # Total height (Z-direction)
thickness = 40.0   # Depth/Thickness (Y-direction)
bore_diam = 25.0   # Diameter of the central hole
chamfer_size = 10.0 # Size of the 45-degree chamfers on corners
gap_size = 2.0     # The visual gap between the top and bottom halves

# Screw hole parameters
hole_diam = 6.5    # Diameter for through holes (clearance for M6 likely)
hole_spacing = 40.0 # Center-to-center distance of holes

# 1. Create the base block
# We create a box centered on the origin
block = cq.Workplane("XY").box(width, thickness, height)

# 2. Add the chamfers
# We select edges parallel to Y (the thickness direction)
# The chamfers are on the top-left, top-right, bottom-left, bottom-right corners
# Looking at the block from the front (XZ plane), these are the corner edges.
result = block.edges("|Y").chamfer(chamfer_size)

# 3. Create the central bore
# A cylindrical cut through the Y-axis
result = result.faces(">Y").workplane().hole(bore_diam)

# 4. Create the vertical mounting holes
# These go through the top face down to the bottom (Z-axis)
# Located on the flat top surfaces created by the chamfer or just on the main body
result = result.faces(">Z").workplane().pushPoints([(-hole_spacing/2, 0), (hole_spacing/2, 0)]).hole(hole_diam)

# 5. Create the horizontal gap
# The image shows a gap running horizontally, splitting the block into top/bottom halves.
# We cut a slot through the center.
# We create a rectangle on the side face and extrude-cut it across.
result = result.faces(">X").workplane().center(0, 0).rect(thickness + 10, gap_size).cutThruAll()

# 6. Refine the top extrusion (The raised "ridge" in the middle)
# The image shows the center section is full height, but the sides where the bolt holes are
# seem slightly lower or chamfered.
# Let's re-examine the image. It looks like the original block shape was actually chamfered 
# heavily on the corners.
# Let's try a different approach to match the specific "ridge" look more accurately.

# Revised Strategy for more accurate geometry:
# 1. Sketch the profile on the Front (XZ) plane.
# 2. Extrude.
# 3. Add holes.

def create_clamp_half(is_top=True):
    # Parameters for half
    h_half = (height / 2) - (gap_size / 2)
    w = width
    t = thickness
    
    # Create the base profile for one half
    # Let's start with a rectangle
    pts = [
        (-w/2, 0),       # Center-line
        (-w/2, h_half - chamfer_size), # Start of chamfer
        (-w/2 + chamfer_size, h_half), # End of chamfer (top)
        (w/2 - chamfer_size, h_half),  # Top right corner
        (w/2, h_half - chamfer_size),  # End of chamfer (side)
        (w/2, 0),        # Bottom right
        (-w/2, 0)        # Close loop
    ]
    
    # Correcting the profile logic: 
    # The image shows an octagon-like profile overall.
    # Let's build a solid block and cut away the corners.
    
    s = cq.Workplane("XY").box(width, thickness, h_half)
    
    # Chamfer the top corners (if is_top) or bottom corners (if not is_top)
    # The selector logic needs to find the correct edges.
    if is_top:
        # Chamfer top edges parallel to Y
        s = s.edges(">Z and |Y").chamfer(chamfer_size)
    else:
        # Chamfer bottom edges parallel to Y
        s = s.edges("<Z and |Y").chamfer(chamfer_size)
        
    # Cut half the bore
    # We cut a half-cylinder from the face that touches the gap (Z=0 plane relative to this part)
    # Actually, simpler to just drill the hole later through the assembly, or cut a semi-circle now.
    
    # Let's orient the cut. For the top half, the cut is on the bottom face.
    cut_plane = "<Z" if is_top else ">Z"
    s = s.faces(cut_plane).workplane().circle(bore_diam/2).cutThruAll()
    
    # Cut the bolt holes
    s = s.faces(">Z").workplane().pushPoints([(-hole_spacing/2, 0), (hole_spacing/2, 0)]).hole(hole_diam)
    
    return s

# Create Top Half
top_half = create_clamp_half(is_top=True)
# Move it up by half the gap size
top_half = top_half.translate((0, 0, gap_size/2))

# Create Bottom Half
bottom_half = create_clamp_half(is_top=False)
# Move it down by half the gap size
bottom_half = bottom_half.translate((0, 0, -gap_size/2))

# Combine them
result = top_half.union(bottom_half)

# Final check of the image:
# The image shows a solid ridge in the middle on the top face?
# Actually, looking closely, it's just a standard octagonal profile clamp.
# The lighting makes the top flat surface look distinct.
# The code above produces the standard profile.

# However, some clamps have a feature where the middle section is higher than the bolt landings.
# Looking at the chamfer, it cuts across the corner.
# If I look at the "ridge" comment in my thought process, maybe the chamfer doesn't go all the way?
# No, looking at the left side, the chamfer is continuous.
# The visual artifact is likely just the lighting on the flat top surface vs the chamfered surface.

# Let's ensure the orientation matches the image.
# Image: Z is up, X is right/left, Y is depth.
# The gap is in the XY plane at Z=0.
# The bore is along the Y axis.

# Code Refinement for simplicity and robustness:
# Instead of building two halves, it is often cleaner to build one block and slice it, 
# but the gap requires material removal.
# The two-half construction method used above is good.

# One specific detail: The image has a "raised" center section? 
# No, that's an optical illusion from the chamfer meeting the flat face. 
# It's a standard Stauff-style pipe clamp geometry.
# Hexagonal/Octagonal exterior.

# Final Code Structure
result = top_half.union(bottom_half)