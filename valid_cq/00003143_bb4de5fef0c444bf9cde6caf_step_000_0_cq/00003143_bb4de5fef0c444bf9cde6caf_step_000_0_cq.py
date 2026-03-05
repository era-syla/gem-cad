import cadquery as cq

# Parametric dimensions
length = 50.0      # Total length of the extrusion
height = 20.0      # Total height of the block
width_bottom = 15.0 # Width of the base
chamfer_size = 5.0 # Size of the top chamfer
slot_radius = 5.0  # Radius of the side groove/slot
slot_height = 8.0  # Height of the center of the slot from the bottom

# Create the base profile sketch on the YZ plane
# We will draw the cross-section and extrude it along the X axis.
# The cross-section is roughly a rectangle with a chamfer on the top-left
# and a circular cutout on the left side.

# Let's define points relative to an origin at the bottom-right corner of the profile
# (looking from the +X direction towards the origin)
# Actually, let's just draw it on the XY plane and extrude in Z for standard orientation,
# then rotate or just assume the axis. Let's stick to the visual:
# Length runs along one axis. The profile is constant.

# Profile definition:
# 1. Start at bottom-right (0,0)
# 2. Line to top-right (0, height)
# 3. Line to top-left (width_bottom, height) -> Actually, let's create a block first.

# Alternative approach: Constructive Solid Geometry (CSG)
# 1. Create a main rectangular block.
# 2. Add the angled face (chamfer) on one top edge.
# 3. Cut the semi-circular groove on the corresponding side face.

# Define the main block dimensions
# Based on visual proportions:
# Length seems ~2.5x height
# Width seems ~0.75x height
L = 60.0  # Length
W = 20.0  # Width (thickness)
H = 30.0  # Height

# Create the basic block
# Let's align it so the length is along X, Height along Z, Width along Y.
base_block = cq.Workplane("XY").box(L, W, H)

# Apply the chamfer to the top edge on the +Y side
# We need to select the edge at (any X, +Y/2, +H/2)
# The chamfer looks significant, maybe 30-45 degrees.
chamfer_edge = base_block.edges(">Z and >Y")
chamfered_block = chamfer_edge.chamfer(H * 0.3)  # Adjust distance as needed

# Create the groove cut
# The groove is on the same side as the chamfer (+Y face).
# It looks like a semi-circular channel running along the X axis.
# Let's create a cylinder to subtract.
groove_radius = H * 0.15
groove_center_z = -H/2 + (H * 0.25) # Positioned near the bottom
groove_center_y = W/2               # On the surface

# Instead of complex selection, let's build the 2D profile and extrude.
# This is often cleaner for this type of shape.

# Profile Points (on YZ plane, extrude along X)
# Origin at bottom-left corner of the profile
p_width = 15.0
p_height = 25.0
p_length = 50.0

# Chamfer parameters
chamfer_d = 8.0 

# Groove parameters
groove_r = 5.0
groove_z_center = 8.0 # Height from bottom

result = (
    cq.Workplane("YZ")
    .moveTo(0, 0)
    .lineTo(p_width, 0)         # Bottom edge
    .lineTo(p_width, p_height - chamfer_d) # Right vertical up to chamfer start
    .lineTo(p_width - chamfer_d, p_height) # Angled top edge (chamfer)
    .lineTo(0, p_height)        # Top edge
    .lineTo(0, 0)               # Left vertical edge
    .close()
    .extrude(p_length)
)

# Now cut the groove on the face that corresponds to the straight vertical side?
# Looking at the image:
# The shape has a large chamfer on one side of the top.
# On the SAME side vertical face below the chamfer, there is a cutout.
# Let's re-examine the image.
# Left side of image: Vertical face with a circular cutout at the bottom, and an angled face at the top.
# Right side of image: Flat vertical face.
# Top: Flat.
# Bottom: Flat.

# So the profile is:
# 1. Start bottom-right (flat side).
# 2. Up to top-right.
# 3. Left across top.
# 4. Angled down-left (chamfer).
# 5. Down vertical (short segment).
# 6. Circular arc inwards (the groove).
# 7. Down vertical to bottom.
# 8. Close to start.

# Let's refine the profile logic using the "front" face seen in the image (actually the end cap).
# Let's assume the face we see is on the YZ plane.

# Dimensions
total_h = 30.0
total_w = 15.0
extrusion_l = 60.0
chamfer_dim = 10.0 # Horizontal and vertical distance for 45 deg chamfer roughly
groove_rad = 4.0
groove_center_h = 8.0

# Build the sketch
res = (
    cq.Workplane("YZ")
    .moveTo(0, 0) # Bottom Left corner
    .lineTo(total_w, 0) # Bottom edge
    .lineTo(total_w, total_h) # Right vertical edge (flat back)
    .lineTo(chamfer_dim, total_h) # Top edge
    .lineTo(0, total_h - chamfer_dim) # Angled chamfer edge
    .lineTo(0, groove_center_h + groove_rad) # Vertical down to top of groove
    # Create the groove arc. It goes inwards.
    .radiusArc((0, groove_center_h - groove_rad), -groove_rad) 
    .lineTo(0, 0) # Vertical down to origin
    .close()
    .extrude(extrusion_l)
)

# Rotate to match the isometric view roughly
# The view has the long axis going back-right. The profile is on the front-left.
# Our extrusion is along X. Y is width, Z is height.
# The profile is in the YZ plane.
result = res