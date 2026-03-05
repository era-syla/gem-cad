import cadquery as cq

# --- Parametric Dimensions ---
# Overall dimensions
height = 60.0
pillar_radius = 15.0
pillar_width = 25.0  # Width of the rectangular back part
pillar_depth = 15.0  # Depth of the rectangular back part
pillar_spacing = 2.0 # Gap between the two main pillars

# Feature details
fin_thickness = 3.0
fin_protrusion = 5.0
num_fins = 3

# Bridge/Connector details
bridge_thickness = 2.0
bridge_setback = 5.0 # How deep the bridge is set from the front face

# Bottom cut details
cut_height = 5.0
cut_depth = 5.0

# --- Helper Function for a Single Pillar ---
def create_pillar(mirror=False):
    # 1. Base Profile: Half-circle front + rectangular back
    # Let's center the profile on the local origin to make mirroring easier later
    
    # Create the rectangular back part
    rect_part = (
        cq.Workplane("XY")
        .rect(pillar_width, pillar_depth, centered=False)
        .translate((-pillar_width/2, -pillar_depth, 0))
    )
    
    # Create the semi-circular front part
    circle_part = (
        cq.Workplane("XY")
        .moveTo(-pillar_width/2, 0)
        .lineTo(pillar_width/2, 0)
        .threePointArc((0, pillar_width/2), (-pillar_width/2, 0)) # Semi-circle
        .close()
    )
    
    # Extrude the base shape
    pillar = (
        rect_part.union(circle_part)
        .extrude(height)
    )

    # 2. Add Fins
    # The image shows fins protruding from the flat side (the "back" in our orientation logic above,
    # or the side facing outwards).
    # Based on the image, the flat faces are the sides, and the rounded face is the front/top.
    # Let's re-orient:
    # Imagine looking from top: ( ) ( )
    # The flat side facing outward has the fins.
    
    # Let's reconstruct the profile logic to match the image better.
    # Profile: A rectangle + a semi-circle on one end.
    # Width of rectangle = radius * 2.
    
    # Revised Pillar construction:
    s = cq.Sketch()
    s = s.segment((0, -pillar_radius), (0, pillar_radius)) # Flat face (inner side)
    s = s.segment((pillar_depth, pillar_radius)) # Side
    s = s.arc((pillar_depth, -pillar_radius), radius=pillar_radius, mode="t") # Rounded front
    s = s.close()
    
    pillar = cq.Workplane("XY").placeSketch(s).extrude(height)

    # 3. Add Fins to the outer side (the rounded side's flat tangent)
    # Actually, looking closely, the fins are on the *flat* side opposite the semi-circle? 
    # No, looking at the right pillar: There is a flat face facing right, with fins.
    # The semi-circle faces "forward" (towards the viewer).
    # The inner face is flat.
    
    # Let's try again with the shape logic based on the right-hand pillar.
    # Inner face: Flat, vertical.
    # Front face: Semi-circle.
    # Outer face: Flat, with fins.
    # Back face: Flat.
    
    # Construction of Right Pillar Profile:
    # Origin at the inner-bottom-front corner.
    profile = (
        cq.Workplane("XY")
        .moveTo(0, 0)
        .lineTo(0, pillar_depth)      # Inner face (going back)
        .lineTo(pillar_width, pillar_depth) # Back face
        .lineTo(pillar_width, 0)      # Outer face
        # Now closing with a 3-point arc or radius for the front
        # The image shows a semi-circle cap on the front.
        # So the main body is a rectangle, with a semi-circle appended to the front (y=0 line)?
        # Let's assume the semi-circle is on top of the Z-axis extrusion? No, it's vertical.
        
        # Let's look at the top face in the image. It's a "D" shape.
        # The flat part of the D is the back? No, the D shapes face each other.
        # Wait, the image shows two columns. The top surface is a semi-circle + rectangle combo.
        # The curved surface is facing the viewer.
        # The flat surfaces between them face each other.
        
        # Correct Geometry Interpretation:
        # Two "D" shaped pillars.
        # The flat sides of the "D"s face each other.
        # The rounded sides face outwards.
        # BUT, the right pillar has fins on a FLAT surface.
        # This implies the shape isn't a simple semi-circle. It's likely a rectangle with a filleted side or a composite shape.
        
        # Alternative Interpretation (most likely):
        # A rectangular block.
        # The front face is rounded (filleted full radius).
        # The inner faces are connected by bridges.
        # The outer faces have fins.
        
        # Let's build the Right Pillar:
        # Rectangle: Width=X, Depth=Y.
        # Front face (Y-min) is fully rounded.
    )
    
    # Right Pillar Construction
    # X axis = Left/Right, Y axis = Front/Back, Z axis = Up/Down
    
    base_rect = cq.Workplane("XY").rect(pillar_width, pillar_depth).extrude(height)
    
    # Round the front face (assuming front is Y-min)
    # Actually, let's make the front face +Y for easier visualization
    # We create a rectangle centered at (0,0)
    # Right pillar center: (pillar_width/2 + gap/2, 0)
    
    # Let's build the right pillar at the origin first
    p_width = 15.0 # Thickness of the slab
    p_depth = 25.0 # Length from flat back to rounded front
    
    # Sketch for Right Pillar
    # Local Origin at the inner edge
    s_right = (
        cq.Workplane("XY")
        .moveTo(0, 0)
        .lineTo(p_width, 0)       # Back face
        .lineTo(p_width, p_depth - p_width/2) # Outer face (straight part)
        .threePointArc((p_width/2, p_depth), (0, p_depth - p_width/2)) # Rounded Front
        .lineTo(0, 0)             # Inner face
        .close()
        .extrude(height)
    )
    
    # Add Fins to the outer face
    # The outer face is the plane at x = p_width
    fin_interval = height / (num_fins + 1)
    
    for i in range(1, num_fins + 1):
        z_pos = height - (i * fin_interval)
        fin = (
            cq.Workplane("YZ")
            .workplane(offset=p_width) # Move to outer face
            .moveTo(0, z_pos)          # Z is now Y in this local plane
            .rect(p_depth + fin_protrusion, fin_thickness, centered=False) # Rough rect
            # Refine fin placement
            .center(0, z_pos)
        )
        # Easier way: simple boxes unioned
        fin_box = (
            cq.Workplane("XY")
            .box(fin_protrusion, p_depth - p_width/2, fin_thickness, centered=(False, False, True))
            .translate((p_width, 0, z_pos))
        )
        s_right = s_right.union(fin_box)

    # Cut the bottom notch on the inner side
    # Inner side is at x=0
    notch = (
        cq.Workplane("XY")
        .box(cut_depth, cut_depth, cut_height, centered=(False, False, False))
        .translate((0, 0, 0)) # Corner notch
    )
    
    # Since the image shows the notch on the inner-back corner (or inner-front?)
    # Looking at the left pillar in the image, the notch is at the bottom corner.
    # Let's assume a notch at the inner-back corner.
    s_right = s_right.cut(notch)

    return s_right

# --- Build Geometry ---

# Parameters refined from visual estimation
p_thick = 15.0  # X dimension of the main body
p_len = 30.0    # Y dimension (including round)
p_height = 80.0
gap = 4.0

# 1. Create Right Pillar
right_pillar = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(p_thick, 0)                       # Back
    .lineTo(p_thick, p_len - p_thick/2)       # Outer Side (straight)
    .threePointArc((p_thick/2, p_len), (0, p_len - p_thick/2)) # Front Round
    .lineTo(0, 0)                             # Inner Side
    .close()
    .extrude(p_height)
)

# 2. Add Fins to Right Pillar
# Fins are on the outer straight face
fin_zs = [25.0, 45.0, 65.0] # Z heights for fins
fin_h = 2.0
fin_stickout = 4.0

for z in fin_zs:
    fin = (
        cq.Workplane("XY")
        .box(fin_stickout, p_len - p_thick/2, fin_h, centered=(False, False, True))
        .translate((p_thick, 0, z))
    )
    right_pillar = right_pillar.union(fin)

# 3. Create Left Pillar (Mirror of Right)
# First translate right pillar to position
right_pillar = right_pillar.translate((gap/2, 0, 0))

# Mirror logic: create left pillar
left_pillar = right_pillar.mirror("YZ")

# 4. Create Bridges/Ribs between pillars
# Bridges are recessed from the rounded front and the flat back
bridge_h = 10.0
bridge_z_positions = [20.0, 40.0, 60.0] # Center Z of bridges (aligned between fins roughly)
bridge_depth = p_len * 0.4 # How deep (Y) the bridge is

for z in bridge_z_positions:
    bridge = (
        cq.Workplane("XY")
        .box(gap + 0.1, bridge_depth, bridge_h, centered=(True, True, True))
        .translate((0, p_len/2 - p_thick/4, z)) # Adjust Y pos to be somewhat centered/recessed
    )
    # Based on image, bridges look like small rectangular tabs connecting the flat inner faces
    # They seem to be aligned with the gaps between fins vertically, or slightly offset.
    # Looking closely at the image:
    # There are vertical slots cut into a solid central block? 
    # Or distinct horizontal bridges?
    # It looks like 3 distinct bridges.
    
    # Let's redefine bridge position based on image
    # They seem to be located at the "back" half of the gap.
    bridge = (
        cq.Workplane("XY")
        .box(gap, 5.0, 8.0, centered=(True, False, True))
        .translate((0, 5.0, z))
    )
    # Actually, simpler to union a block and cut slots
    pass

# Alternative Strategy: Create the two pillars, then add the connecting material.
# The image shows a continuous central connection with slots cut out.
# Or separate bridges. Let's assume separate bridges for cleaner code.
# The bridges are thin vertically.

bridges = cq.Workplane("XY")
bridge_positions_z = [35.0, 55.0] # The "fins" on the side seem to align with solid parts? 
# Let's align bridges with the fins roughly.
# Fin Zs were 25, 45, 65.
# Bridges seem to be connecting the inner faces.
bridge_width = 4.0 # Y direction width
bridge_thick = 20.0 # Z direction height (they look tall in the gap)
# Looking at the gap: it's a vertical slot, interrupted by material?
# No, it looks like a solid wall with rectangular holes (slots) cut into it.

# Let's try the "Solid Wall with Slots" approach for the middle.
# Create a wall filling the gap
wall = (
    cq.Workplane("XY")
    .box(gap, p_len/2, p_height, centered=(True, False, False))
    .translate((0, 0, 0))
)

# Cut slots into the wall
slot_height = 12.0
slots = (
    cq.Workplane("XZ")
    .workplane(offset=-10) # In front of the model
    .moveTo(0, 15)
    .rect(gap*2, slot_height)
    .moveTo(0, 35)
    .rect(gap*2, slot_height)
    .moveTo(0, 55)
    .rect(gap*2, slot_height)
    .extrude(100) # Cut through
)

# Apply slots to the "wall" idea?
# Actually, looking at the image:
# The gap has "teeth".
# Let's model 3 specific connector blocks.
connector_z = [25.0, 45.0, 65.0] # Same Z as fins
connector_block = (
    cq.Workplane("XY")
    .box(gap, 6.0, 4.0, centered=(True, False, True))
)

connectors = cq.Workplane("XY")
for z in connector_z:
    c = connector_block.translate((0, 2.0, z)) # Set back slightly from flat face
    connectors = connectors.union(c)

# 5. Bottom Cutout
# There is a rectangular cutout at the bottom of the pillars on the inner side.
cutout_sz = 6.0
cutout_h = 6.0

# Cut left pillar bottom inner corner
cut_left = (
    cq.Workplane("XY")
    .box(cutout_sz, cutout_sz, cutout_h, centered=(True, True, False))
    .translate((-gap/2, 0, 0)) # Centered on the inner edge
)
# Cut right pillar bottom inner corner
cut_right = (
    cq.Workplane("XY")
    .box(cutout_sz, cutout_sz, cutout_h, centered=(True, True, False))
    .translate((gap/2, 0, 0))
)


# --- Final Assembly ---
result = right_pillar.union(left_pillar)
result = result.union(connectors)
result = result.cut(cut_left).cut(cut_right)

# Refine the bridges based on closer inspection
# The bridges look flush with the back face?
# Let's adjust connectors to be flush with back (Y=0)
connectors_refined = cq.Workplane("XY")
for z in connector_z:
    # Small bridge connecting the flat faces
    c = (
        cq.Workplane("XY")
        .box(gap, 5.0, 3.0, centered=(True, False, True)) # width, depth, height
        .translate((0, 2.5, z)) # Flush with back (Y=0) + slight offset to match image depth
    )
    connectors_refined = connectors_refined.union(c)

# Re-assemble with refined connectors
result = right_pillar.union(left_pillar)
result = result.union(connectors_refined)

# The cutout at the bottom seems to go through the back face as well
# Make the cutout a box on the corner
corner_cut = (
    cq.Workplane("XY")
    .box(cutout_sz, cutout_sz, cutout_h, centered=(False, False, False))
    .translate((-gap/2 - cutout_sz, 0, 0)) # Left side cut
)
corner_cut_2 = (
    cq.Workplane("XY")
    .box(cutout_sz, cutout_sz, cutout_h, centered=(False, False, False))
    .translate((gap/2, 0, 0)) # Right side cut
)

result = result.cut(corner_cut).cut(corner_cut_2)

# Rotate to match image orientation roughly (Isometric view is automatic in most viewers, 
# but upright is Z)
# The image shows Z up.

# Final check of image features:
# - Rounded tops? No, the top face is flat, the profile is rounded. Correct.
# - Fins on outer edges? Yes.
# - Connectors in middle? Yes.
# - Notch at bottom? Yes.

# One detail: The connectors in the middle look like they might correspond to the fins, 
# but the image shows the gap has 3 "teeth" or bridges. 
# My code has 3 bridges aligned with fins.

# One correction: The image shows the fins are located on the BACK side (the flat side opposite the curve)?
# No, looking at shadow, the curve is the front. The side wall is flat. The fins stick out of the side wall.
# My model reflects this.

# Final Code Generation
result = result