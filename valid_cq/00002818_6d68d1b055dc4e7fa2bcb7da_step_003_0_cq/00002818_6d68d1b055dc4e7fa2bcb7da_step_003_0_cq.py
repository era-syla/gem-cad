import cadquery as cq

# --- Parameters ---
# Overall dimensions
length = 100.0  # Total length of the bracket
width = 30.0    # Width of the top face
height = 30.0   # Height of the vertical back face
thickness = 5.0 # Wall thickness if we were shelling, but here it defines the "solid" depth at the tip

# Hole parameters
hole_diameter = 5.0
num_holes = 4
hole_spacing = length / num_holes
hole_start_offset = hole_spacing / 2.0  # Center holes in their segments

# Slot parameters
slot_width = 5.0
slot_depth = 10.0
slot_fillet_radius = slot_width / 2.0 # To make the top of the slot round

# --- Geometry Construction ---

# 1. Create the base triangular profile and extrude it
# We sketch on the YZ plane (side view) and extrude along X
# The profile is a right triangle with a flat bottom tip (trapezoidal prism effectively)
# Points: (0,0), (width, 0), (0, -height) -> This is a simple triangle. 
# Looking at the image, the bottom tip is actually sharp or very slightly flat.
# Let's assume a standard right-angle bracket shape.
# (0,0) is top-left corner on the side view.
# We will draw a right triangle on the YZ plane.

pts = [
    (0, 0),          # Top-left (back corner)
    (width, 0),      # Top-right (front edge)
    (0, -height)     # Bottom-left (bottom tip)
]

# Create the main wedge body
base_wedge = (
    cq.Workplane("YZ")
    .polyline(pts)
    .close()
    .extrude(length)
)

# 2. Add the holes on the top face
# We select the top face. The top face is on the XY plane relative to the extrusion?
# Since we extruded along X from YZ, the top face is roughly defined by y=0.
# However, CadQuery extrusion usually centers or starts at origin. 
# Let's verify orientation.
# "YZ" plane extrude(length) -> X axis is the extrusion direction.
# Top edge was (0,0) to (width,0). So the top face is on the plane Z=0 (local to sketch), 
# which corresponds to the global XZ plane relative to the sketch?
# Actually, let's just select the face by direction.
# The top face normal is likely +Z or +Y depending on how 'polyline' coordinates map.
# In YZ plane: Y is horizontal, Z is vertical usually in CQ Workplane("YZ").
# Let's re-orient for clarity:
# Use Workplane("XY") for the base sketch to make Z-extrusion? 
# No, let's stick to the visual orientation.
# Let's assume the length runs along X. The cross section is in YZ.
# Top face is parallel to XZ plane? No, top face is flat.
# Let's assume:
#   Length along X axis.
#   Width along Y axis.
#   Height along Z axis.

# Let's build it as a block and cut the angle.
# Box dimensions: length x width x height
base_block = cq.Workplane("XY").box(length, width, height, centered=False)

# Now we cut the angle. We want a right triangle cross section.
# We want to keep the top face (Z=height) and the back face (Y=width or Y=0?).
# Let's center the box on X, but align Y and Z for easier reasoning.
# Center=False puts corner at 0,0,0.
# Box covers x: 0..100, y: 0..30, z: 0..30.
# We want to slice off a triangle.
# We want to keep the face at Z=30 (top) and Y=0 (back vertical face).
# So we want to remove the material below the diagonal connecting (y=0, z=0) to (y=30, z=30)?
# Wait, looking at the image:
# Top face is flat. Back face is vertical. Front face is slanted.
# So at Y=0 (back), Z goes from 0 to 30.
# At Y=30 (front), Z is 30.
# This would make the slope go UP towards the front.
# The image shows a wedge where the thick part is at the back/top.
# Let's try:
# Back face: Y=width (thickest part). Front edge: Y=0 (thinnest part).
# Top face: Z=height.
# So we want points: (Y=0, Z=height), (Y=width, Z=height), (Y=width, Z=0).
# This creates a wedge with a vertical back at Y=width.

# Let's restart the construction with a cleaner approach using a sketch extrusion.
# Profile on Right plane (YZ), extruded along X.
# Sketch points: (0,0) -> (width, 0) -> (0, -height) -> close.
# (0,0) is top-back. (width, 0) is top-front. (0, -height) is bottom-back.
# This creates a wedge where the top surface is on the XY plane (local), back is vertical along Z.
result = (
    cq.Workplane("YZ")
    .polyline([(0, 0), (width, 0), (0, -height)])
    .close()
    .extrude(length)
)

# Re-orient the part so it sits nicely (optional, but good for visualization)
# Currently extrusion is along +X.
# The top face is on the local plane defined by the line (0,0)-(width,0).
# In global coords, the top face is at Z=0? No, let's just work relative to faces.

# 3. Create Holes on Top Face
# Find the top face. It is the face with normal closest to +Z? 
# In the sketch (YZ), top edge is horizontal (Y axis). Extrusion is X. 
# So top face normal is +Z? Wait, YZ plane means Y is horiz, Z is vert.
# My points were (0,0), (width, 0), (0, -height).
# The segment (0,0)-(width,0) is along the local X-axis of the sketch plane?
# Workplane("YZ"): Local X is Global Y, Local Y is Global Z.
# Points: (y=0, z=0), (y=width, z=0), (y=0, z=-height).
# Top edge is on local Z=0 (Global Z=0).
# Extrusion is Global X.
# So Top Face is on the Global X-Y plane (Z=0).
# Let's select it by normal direction (0, 0, 1) or simply the largest face in +Z or similar.
# Actually, the face is at Z=0. But normal points "out".
# Since the solid is below Z=0 (z goes to -height), the top face normal is +Z.

# Calculate center points for holes
hole_centers = []
for i in range(num_holes):
    x_pos = (i * hole_spacing) + hole_start_offset
    # Center in Y direction (width)
    y_pos = width / 2.0
    hole_centers.append((length - x_pos, y_pos)) # Adjust X because extrude goes 0->length

# Apply holes
result = (
    result
    .faces(">Z") # Select top face
    .workplane()
    .pushPoints(hole_centers)
    .hole(hole_diameter)
)

# 4. Create Slots on the Slanted Face
# The slots cut through the slanted face and seem to go vertically upwards?
# Looking closely at the image:
# The slots are U-shaped cutouts at the bottom edge of the back/vertical face?
# No, looking at the orientation, the vertical face is in shadow. The slanted face is facing us.
# The slots are on the slanted face, cutting upwards from the bottom edge.
# They look like they are cut perpendicular to the bottom edge, or vertically relative to the global orientation.
# The top of the slot is rounded.
# The slots align with the holes? 
# In the image, there are 4 holes and 4 slots. They seem aligned vertically.

# We need to cut these slots.
# Easiest way is to sketch the slot profile on the back vertical face (or a plane parallel to it) and cut through.
# Back vertical face is at local y=0 in sketch -> Global Y=0? 
# In my sketch: (0,0), (width,0), (0,-height).
# The vertical leg is from (0,0) to (0,-height). This corresponds to Global Y=0.
# So the back face is on the XZ plane at Y=0.
# Let's select the back face ("<Y") and sketch the U-shapes.

slot_centers = []
for i in range(num_holes):
    x_pos = (i * hole_spacing) + hole_start_offset
    # Z position: starting from bottom edge (-height) going up.
    # We define the center of the arc at the top of the slot.
    # Slot goes from bottom z=-height up to z=(-height + slot_depth).
    # But wait, sketch coordinates on the back face.
    # Face <Y is the XZ plane.
    # X axis is global X (0 to length).
    # Y axis is global Z (0 to -height).
    # Center of slot in X is same as holes: (length - x_pos).
    # Center of slot top arc in Y (Global Z) is: -height + slot_depth.
    slot_centers.append((length - x_pos, -height + slot_depth))

# We will cut these shapes through the entire part in the Y direction, 
# or just deep enough? The image shows them cutting through the thin edge.
# The slots are on the "bottom" sharp edge.
# Let's perform a cut through all.

# Create the cutting profile for one slot
# It's a U shape.
# We'll use a custom profile.
def slot_profile(loc):
    x, z = loc.toTuple() # Center of the top circle
    # Points relative to center
    return (
        cq.Workplane()
        .moveTo(x - slot_width/2, -height) # Start at bottom left of slot on face
        .lineTo(x - slot_width/2, z)       # Line up to arc start
        .threePointArc((x, z + slot_width/2), (x + slot_width/2, z)) # Top arc
        .lineTo(x + slot_width/2, -height) # Line down
        .close()
    )

# It's easier to just draw rectangles and fillet them, or use the slot tool if applicable?
# CadQuery `slot2D` makes a stadium shape (full slot), we have an open slot at the bottom.
# Let's just make rectangular cuts and then fillet the top corners? 
# Or just cut the U-shape explicitly.

# Let's use rects and fillets for robustness.
# Draw rectangles on the back face, extrude/cut, then fillet.
# Rect center Y (Global Z): -height + slot_depth/2
# Rect height: slot_depth
# Rect width: slot_width
result = (
    result
    .faces("<Y") # Select back face (XZ plane essentially)
    .workplane() # Origin likely at corner
)

# We need to be careful with coordinates on the selected face.
# Let's push points for the slot centers and draw rectangles.
# Centers for rects:
rect_centers = []
for i in range(num_holes):
    x_pos = (i * hole_spacing) + hole_start_offset
    # Center of the rectangle
    # X: length - x_pos
    # Y (local, global Z): -height + (slot_depth / 2.0)
    rect_centers.append((length - x_pos, -height + (slot_depth / 2.0)))

result = (
    result
    .pushPoints(rect_centers)
    .rect(slot_width, slot_depth)
    .cutThruAll() # Cut through the wedge
)

# Now apply fillets to the tops of the slots.
# We need to select the edges at the top of the cutouts.
# This can be tricky with selectors.
# The top face of the slot cut is a cylindrical surface if we cut a full slot, 
# but here it's a flat face because we cut a rect.
# We want to fillet the two vertical edges inside the slot? No, the top horizontal edge inside the slot?
# Actually, the slot shape in the image is a "U". 
# The cut I made is a rectangle. 
# So the top of the hole is flat. I need to fillet the two upper corners of the rectangle cut.
# However, `cutThruAll` makes a 3D cut.
# It's probably easier to cut the U-shape directly sketch-wise.

# Let's rollback the rect cut and do a proper U-shape cut.
# Construct the U-shape profile wire.
# We iterate to accumulate the shapes in the sketch.

# Re-establish Workplane on back face
wp = result.faces("<Y").workplane()

for i in range(num_holes):
    x_pos = (length) - ((i * hole_spacing) + hole_start_offset)
    # Bottom of slot is at global Z = -height.
    # Top of linear part is at global Z = -height + slot_depth - radius
    # Radius = slot_width / 2
    r = slot_width / 2.0
    z_bottom = -height
    z_top_center = -height + slot_depth
    z_straight_top = z_top_center - r
    
    # Draw U-shape
    # Start bottom-left of slot
    wp = (
        wp
        .moveTo(x_pos - r, z_bottom)
        .lineTo(x_pos - r, z_top_center) # Left vertical
        .radiusArc((x_pos + r, z_top_center), r) # Top arc 180 deg? radiusArc endpoint, radius
        # radiusArc can be tricky with 180 deg. threePointArc is safer.
        # Top point: (x_pos, z_top_center + r)
        # End point: (x_pos + r, z_top_center)
        # .threePointArc((x_pos, z_top_center + r), (x_pos + r, z_top_center))
        .lineTo(x_pos + r, z_bottom) # Right vertical
        .close()
    )

# Perform the cut
result = wp.cutThruAll()

# 5. Fillets/Chamfers (Optional based on image)
# The image shows sharp edges mostly, maybe very slight chamfer on holes. 
# The tip of the wedge (bottom edge) looks slightly blunt, but my profile handles that if dimensions are right.
# The image looks like the slots have a rounded top (handled).
# The holes are countersunk? 
# They look like simple through holes, maybe slight chamfer.
# I'll stick to simple holes as requested by generic "model based on image".

# Ensure result is returned
result = result