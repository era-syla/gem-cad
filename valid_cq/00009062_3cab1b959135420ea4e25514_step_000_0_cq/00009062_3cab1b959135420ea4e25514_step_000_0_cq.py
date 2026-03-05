import cadquery as cq

# --- Parametric Variables ---
# Aluminum Profile Parameters (approximate typical T-slot profile)
profile_width = 40.0
profile_height = 40.0
profile_length = 50.0  # Length of the extrusion segment
slot_width = 6.0
slot_depth = 6.0
corner_radius = 2.0
center_hole_dia = 5.0
# The profile has distinct "teeth" or ribs. Let's approximate the complexity.

# Connector Block Parameters
block_length = 40.0
block_width = 40.0
block_height = 40.0  # Main body height
step_height = 10.0   # The raised portion
step_length = 20.0
hole_dia_side = 6.0  # Large countersunk hole
hole_cbore_dia = 12.0
hole_cbore_depth = 3.0
top_small_hole_dia = 3.0
top_rect_hole_w = 4.0
top_rect_hole_l = 6.0

# --- Helper Function for Profile Geometry ---
def create_profile_sketch():
    """
    Creates a detailed sketch of a 40x40 extrusion profile cross-section.
    This is an approximation of a generic T-slot profile.
    """
    w = profile_width
    h = profile_height
    s_w = slot_width
    s_d = slot_depth
    
    # Outer box with rounded corners
    pts = [
        (w/2, h/2), (w/2, -h/2), (-w/2, -h/2), (-w/2, h/2)
    ]
    
    # Create the main body
    base = cq.Sketch().rect(w, h).vertices().fillet(corner_radius)
    
    # Create the slots (T-slots)
    # North
    n_slot = (
        cq.Sketch()
        .push([(0, h/2)])
        .rect(s_w, s_d*2) # Main slot opening
        .push([(0, h/2 - s_d/2)]) 
        .rect(s_w*2, s_d) # Inner T wide part
    )
    
    # Create one generic slot cutter shape to rotate and place
    # A standard T-slot has an opening and a wider cavity
    t_neck = s_w
    t_cavity_w = s_w * 2.5
    t_cavity_h = s_d 
    
    # Helper to cut slots from four sides
    slot_cutter = cq.Sketch()
    for angle in [0, 90, 180, 270]:
        # Define T-slot geometry relative to center, then rotate/translate
        # This is a simplified approach: just cut rectangles from edges
        dx = (w/2) 
        if angle == 90 or angle == 270: dx = h/2
            
        # We'll subtract rectangles from the base
        # Neck
        slot_cutter = slot_cutter.rect(t_neck, w*2, angle=angle) # Through cut for neck
        
        # Inner Cavity (approximate)
        # We need to position these carefully. 
        # Easier method: construct a single slot shape and rotate/copy
        pass

    # Let's build the profile by subtraction from a solid block for better control
    # or define a detailed polygon. Given the request, constructing a reasonably accurate
    # visual representation via subtraction is robust.
    return base

# --- Modeling Phase ---

# 1. Create the Aluminum Extrusion
# We define the cross-section by taking a square and subtracting slots
extrusion_sketch = cq.Workplane("YZ") # Orient along X-axis visually
base_ext = extrusion_sketch.rect(profile_width, profile_height).extrude(profile_length)

# Define a T-slot cutter profile (Side view)
# Neck
slot_neck_w = 8.0
slot_inner_w = 15.0
slot_depth = 9.0
slot_neck_depth = 4.0

# Function to cut a slot on a face
def cut_t_slot(part, workplane_str, offset_val):
    # This cuts the longitudinal slots along the length of the extrusion
    # Since we extruded along X (normal to YZ), the long faces are Top, Bottom, Front, Back relative to the extrusion local coords
    
    # Actually, let's just make the sketch complex and extrude once, it's cleaner.
    pass

# Improved Extrusion Construction
s = cq.Sketch()
# Outer perimeter with fillets
s = s.rect(profile_width, profile_height)
s = s.vertices().fillet(2.0)

# Cut Center Hole
s = s.circle(center_hole_dia/2, mode='s')

# Cut T-Slots (North, South, East, West)
for angle in [0, 90, 180, 270]:
    # Distance from center to edge
    edge_dist = profile_width / 2.0
    
    # T-Slot geometry
    # Neck
    s = s.push([(0, 0)]).rect(6.0, profile_height + 10, angle=angle, mode='s') 
    
    # Inner Cavity
    cavity_offset = edge_dist - 3.0 # Depth from surface
    
    # We need to rotate the offset vector
    import math
    rad = math.radians(angle)
    dx = (edge_dist - 4.0) * math.cos(rad) # rough depth
    dy = (edge_dist - 4.0) * math.sin(rad)
    
    if angle in [0, 180]:
        rect_w, rect_h = 4.0, 12.0 # Cavity dimensions
    else:
        rect_w, rect_h = 12.0, 4.0
        
    # Simplify: Just cut intersecting rectangles for the visual look of the extrusion
    # Corner grooves
    corner_offset = profile_width/2
    s = s.push([(corner_offset, corner_offset), (corner_offset, -corner_offset), 
                (-corner_offset, corner_offset), (-corner_offset, -corner_offset)])
    s = s.rect(2.0, 2.0, mode='s') # Small notches in corners

# Create the solid extrusion
extrusion = cq.Workplane("YZ").placeSketch(s).extrude(profile_length)

# Add Ribs/Grooves to the extrusion faces for realism (visual texture)
# We will cut small grooves along the length
groove_r = 0.5
for face in [">Z", "<Z", ">Y", "<Y"]:
    # Create a profile on the end face to sweep or cut? No, just cut rectangles.
    # It's perpendicular to the extrusion axis (X).
    # Let's simplify: The image shows the end-grain profile.
    pass 
    # The sketch `s` defines the shape. To get the ribbed look in the image,
    # we can modify the sketch `s` to be more jagged, but that's complex.
    # Let's stick to the main T-slot shape which is recognizable.


# 2. Create the Connector Block
# The block sits "behind" or attached to the extrusion.
# Based on image, it looks like a clamp or mount.
# It has an L-shape or stepped shape.

block_base = cq.Workplane("XY").workplane(offset=-block_length/2) \
    .box(block_length, block_width, block_height, centered=(True, True, False))

# Cut the step to make the L-shape
# The step removes material from the top-front
cut_step = (
    cq.Workplane("XY")
    .workplane(offset=block_height - step_height)
    .rect(block_length, block_width) # oversized to ensure cut
    .extrude(step_height)
    .translate((step_length/2, 0, 0)) # Shift to cut half
)

# Actually, construct additively is easier for the stepped shape
# Base Part (The taller back section)
part2_back = (
    cq.Workplane("XY")
    .box(block_length/2, block_width, block_height, centered=(False, True, False))
    .translate((-block_length/2, 0, 0))
)

# Front Part (The shorter front section)
part2_front = (
    cq.Workplane("XY")
    .box(block_length/2, block_width, block_height - step_height, centered=(False, True, False))
)

connector = part2_back.union(part2_front)

# Add holes to connector
# Large side countersunk hole (on the taller part)
connector = (
    connector.faces(">X")
    .workplane()
    .center(0, block_height/2) # Local coords might be tricky, centering on face
    .moveTo(0, 0) # Center of the face
    # Adjust position visually based on image: centered vertically on the tall part
    .cboreHole(hole_dia_side, hole_cbore_dia, hole_cbore_depth)
)

# Top small round hole (on the shorter part)
connector = (
    connector.faces(">Z[1]") # Select the lower top face (the step)
    .workplane()
    .pushPoints([(-block_length/4 + 5, 0)]) # Slight offset
    .hole(top_small_hole_dia)
)

# Top rectangular slot/hole (on the shorter part)
connector = (
    connector.faces(">Z[1]")
    .workplane()
    .pushPoints([(block_length/4 - 5, 0)])
    .rect(top_rect_hole_w, top_rect_hole_l)
    .cutBlind(-10)
)

# Split line indication (Image shows a split line, suggesting a clamp)
# We can create a thin cut through the middle of the tall part
split_cut = (
    cq.Workplane("XY")
    .box(block_length/2, 0.5, block_height, centered=(False, True, False))
    .translate((-block_length/2, 0, 0))
)
connector = connector.cut(split_cut)


# 3. Assembly / Positioning
# The extrusion passes through the connector or is mounted to it.
# In the image, the extrusion is in the foreground, perpendicular to the connector's axis.
# The connector shape in the image actually seems to WRAP the extrusion profile somewhat, 
# or match its profile. Let's assume the "Front Part" of the connector has a profile cutout.

# Rotate Extrusion to match image (Extrusion runs along an axis, Connector runs perpendicular)
# Image: Extrusion axis is roughly X/Y diagonal. Connector is vertical block.
# Let's orient Extrusion along X, Connector generally along Y/Z.

# Re-orient extrusion
extrusion_final = extrusion.translate((-profile_length/2, 0, 0))

# Re-orient Connector
# The connector seems to clamp onto the side of the extrusion.
# Let's rotate the connector to sit "behind" the extrusion.
connector_final = (
    connector
    .rotate((0,0,0), (0,0,1), 90) # Rotate around Z
    .translate((0, profile_width/2 + block_width/2, 0)) # Move behind in Y
)

# Adjusting purely based on the specific image isometric view:
# The extrusion end is visible. 
# The connector is attached to the side face of the extrusion.
# The connector has a hole facing the viewer (on the right).

# Let's rebuild the connector in place relative to the extrusion for better parametric linkage.
# Connector mounts to the Right face (+Y) of the extrusion.
connector_block = (
    cq.Workplane("XZ") # Draw on plane perpendicular to Y
    .workplane(offset=profile_width/2) # Move to surface of extrusion
    .box(block_length, block_height, block_width, centered=(True, True, False)) # Extrude outwards in Y
)

# Add the step to the connector block (The top part is lower)
# The block in the image has a step down on the left side (relative to the hole face).
# Let's cut a chunk out.
cutter = (
    cq.Workplane("XZ")
    .workplane(offset=profile_width/2 + block_width - step_height) # Start cut from top (which is Y max)
    .rect(block_length/2, block_height + 2) # Cut half the width
    .extrude(step_height + 2) # Cut downwards
    .translate((-block_length/4, 0, 0)) # Shift to left side
)

# Re-implementing Connector Geometry to match image precisely
# The connector is a block attached to the side.
# Dimensions
c_len = 50.0 # Length along Extrusion axis
c_h = 45.0   # Height Z
c_thk = 30.0 # Thickness coming off the extrusion (Y)

# Base block
c_base = (
    cq.Workplane("XY")
    .box(c_len, c_thk, c_h, centered=(True, False, True))
    .translate((0, profile_width/2, 0)) # Position against extrusion face
)

# The "Step": The left side (negative X) is lower.
cut_box = (
    cq.Workplane("XY")
    .box(c_len/2, c_thk, c_h/2, centered=(False, False, False)) # Box to remove top-left
    .translate((-c_len/2, profile_width/2, 0)) # Position: Left, against extrusion, from Z=0 up
)
# Actually, looking at the image, the connector is TALLER on the right, SHORTER on the left.
# So we cut the top-left quadrant relative to the view.
# Let's cut the top of the left side.
step_cut = (
    cq.Workplane("XY")
    .workplane(offset=10) # Height of the lower shelf
    .box(c_len/2 + 1, c_thk + 1, c_h) # Large box to clear everything above
    .translate((-c_len/4 - 0.5, profile_width/2 + c_thk/2, 0))
)
c_base = c_base.cut(step_cut)

# The large hole on the right face (Tall part)
# Face is +X face of the connector block? No, it's the face parallel to extrusion axis?
# Image: Hole is on the face perpendicular to the extrusion axis.
# The connector is attached to the *End*? No, looks like the side.
# Let's assume the hole axis is perpendicular to the extrusion axis (Y axis).
c_base = (
    c_base.faces(">X")
    .workplane()
    .center(0, -5) # Lower down slightly
    .cboreHole(6.0, 14.0, 4.0)
)

# The split line on the tall part
split = (
    cq.Workplane("YZ")
    .rect(c_thk, c_h)
    .extrude(0.5)
    .translate((c_len/4, profile_width/2 + c_thk/2, 0))
)
# c_base = c_base.cut(split) # Optional detail, sometimes messy with overlap

# Small hole on the step (Left side)
c_base = (
    c_base.faces(">Z").filter(lambda f: f.BoundingBox().center.x < 0) # Select the lower face
    .workplane()
    .center(-5, 5)
    .hole(4.0)
)

# Rectangular slot on the step
c_base = (
    c_base.faces(">Z").filter(lambda f: f.BoundingBox().center.x < 0)
    .workplane()
    .center(5, -2)
    .rect(4.0, 6.0)
    .cutBlind(-15.0)
)


# Combine Extrusion and Connector
result = extrusion.union(c_base)

# Visual polish: Fillet the extrusion outer edges slightly more for the "ribbed" look illusion
# (Skipped for code simplicity as generic fillets on complex sketches fail easily)

# Final Result
result = result