import cadquery as cq

# --- Parametric Dimensions ---
# Overall frame dimensions
frame_width = 80.0
frame_height = 80.0
thickness = 10.0

# Central opening dimensions (irregular shape)
# The opening is roughly rectangular but with chamfered/angled corners
# especially on the left side to accommodate the pointed outer shape.
wall_thickness = 10.0

# The left side feature (pointed extrusion)
point_offset = 20.0  # How far the point sticks out from the main rectangle

# Tabs (top and bottom)
tab_width = 10.0
tab_height = 8.0  # Height sticking out from frame
tab_spacing = 25.0 # Center-to-center spacing (roughly)

# Holes
side_hole_diameter = 6.0
point_hole_diameter = 5.0

# --- Geometry Construction ---

# 1. Base Shape: The main outer profile including the pointed left side
# Let's define the vertices of the outer perimeter
# We assume the right side is vertical, top/bottom horizontal, left side pointed.
# Origin at center of the main "rectangle" part.

# Calculate vertices relative to center
half_w = frame_width / 2.0
half_h = frame_height / 2.0
point_x = -half_w - point_offset

# Define the 2D sketch for the outer profile
pts_outer = [
    (half_w, half_h),           # Top Right
    (point_x, 0),               # Left Point
    (half_w, -half_h),          # Bottom Right
]

# Create the base extrusion
# We use a polyline for the angled left side and straight lines for right
base_profile = (
    cq.Workplane("XY")
    .moveTo(half_w, half_h)
    .lineTo(half_w, -half_h)
    .lineTo(-half_w, -half_h)
    .lineTo(point_x, 0)
    .lineTo(-half_w, half_h)
    .close()
    .extrude(thickness)
)

# 2. Cut the central hole
# The hole shape follows the outer contour but with wall thickness
# It seems to have a large chamfer on the inner left corners
inner_half_w = half_w - wall_thickness
inner_half_h = half_h - wall_thickness
# The inner left side is vertical, unlike the outer pointed side
inner_left_x = -half_w + wall_thickness

# There is also an angled cut on the inside right
# Let's approximate the inner shape based on the image:
# It looks like a rectangle with chamfered corners on the left
# and a slight angle on the right wall? Actually, looking closer at the image:
# - The right inner wall is vertical.
# - The top and bottom inner walls are horizontal.
# - The left inner wall has two angled segments corresponding to the outer point, 
#   but truncated to be vertical in the middle? 
#   Let's look at the "right" side of the image (actually the flat side). 
#   Wait, looking at the right side of the image (the flat vertical side), there is a hole there.
#   Looking at the left side (the pointed side), there is a hole through the point.

# Let's simplify the inner cutout to match the visual style:
# A large rectangle, with chamfers on the corners near the "pointy" side.

cutout_shape = (
    cq.Workplane("XY")
    .rect(frame_width - 2*wall_thickness, frame_height - 2*wall_thickness)
    .extrude(thickness)
)

# However, the image shows the inner left corners are heavily chamfered/angled 
# to leave material for the point mechanism.
# Let's refine the cutout.
# Inner right x: inner_half_w
# Inner top y: inner_half_h
# The cutout seems to be a polygon.
pts_inner = [
    (inner_half_w, inner_half_h),   # Top Right
    (inner_half_w, -inner_half_h),  # Bottom Right
    (inner_left_x, -inner_half_h),  # Bottom Left (start of chamfer?)
    # Actually, looking at the image, the inner shape is an octagon/chamfered rect
    # Let's just chamfer the rectangle edges after cut or define points.
]

# Let's try cutting a simple rectangle first, then adding material back or cutting corners?
# Better: Define exact points for the hole.
# The hole seems to have vertical right wall, horizontal top/bottom, 
# and the left side follows the outer angle but offset.
inner_point_x = point_x + wall_thickness * 1.5 # approximate offset
# But looking closely, the inner left wall is vertical for a bit? No, it looks just angled.
# Let's define the cutout polygon.

cutout_wire = (
    cq.Workplane("XY")
    .moveTo(inner_half_w, inner_half_h) # Top Right
    .lineTo(inner_half_w, -inner_half_h) # Bottom Right
    .lineTo(-half_w + wall_thickness, -inner_half_h) # Bottom Left (straight part)
    .lineTo(-half_w + wall_thickness + 10, -inner_half_h + 10) # Chamfer?
    # Let's make it simpler: A rectangle with chamfers on the left corners.
)

# Re-evaluating geometry based on shadows:
# The main body is a frame. 
# Right side: Thick vertical bar.
# Top/Bottom: Horizontal bars.
# Left side: Angled bars meeting at a point.

result = base_profile

# Create the inner cutout
# Using a loft or just straight extrusion of a shape.
# Let's define the inner shape points to create the "frame" look.
inner_pts = [
    (half_w - wall_thickness, half_h - wall_thickness), # TR
    (half_w - wall_thickness, -half_h + wall_thickness), # BR
    (-half_w + wall_thickness, -half_h + wall_thickness), # BL (inner corner)
    # The inner cutout has chamfers on the left side to follow the outer point shape
    (point_x + wall_thickness*1.5, 0), # Middle Left (inner point)
    (-half_w + wall_thickness, half_h - wall_thickness) # TL
]
# Refined Inner Shape: The image actually shows the inner hole is roughly rectangular 
# with large chamfers on the left side corresponding to the point structure.
inner_sketch = (
    cq.Workplane("XY")
    .moveTo(half_w - wall_thickness, half_h - wall_thickness)
    .lineTo(half_w - wall_thickness, -half_h + wall_thickness)
    .lineTo(-half_w + wall_thickness + 10, -half_h + wall_thickness) # Bottom flat
    .lineTo(point_x + 35, 0) # Angled in
    .lineTo(-half_w + wall_thickness + 10, half_h - wall_thickness) # Top flat
    .close()
    .extrude(thickness)
)
# Note: The visual implies the inner left side is just a chamfered rect.
# Let's go with a chamfer operation on the internal faces of a rect cut? 
# Hard to select. Let's stick to drawing the cut.

# Let's rebuild the main shape more robustly as a single sketch with subtraction.
full_sketch = (
    cq.Workplane("XY")
    # Outer wire
    .moveTo(half_w, half_h)
    .lineTo(half_w, -half_h)
    .lineTo(-half_w, -half_h)
    .lineTo(point_x, 0)
    .lineTo(-half_w, half_h)
    .close()
    
    # Inner wire (the hole)
    # Based on the image, the hole looks like a rectangle with the left side 
    # modified to be trapezoidal/chamfered.
    .moveTo(half_w - wall_thickness, half_h - wall_thickness)
    .lineTo(-half_w + wall_thickness, half_h - wall_thickness)
    .lineTo(-half_w + wall_thickness - 5, 0) # Slight bump out or straight?
    # Actually, let's just make a rectangular cut and chamfer the result.
    # It's safer.
)
result = (
    cq.Workplane("XY")
    .moveTo(half_w, half_h)
    .lineTo(half_w, -half_h)
    .lineTo(-half_w, -half_h)
    .lineTo(point_x, 0)
    .lineTo(-half_w, half_h)
    .close()
    .extrude(thickness)
)

# Cut the central rectangular hole
result = result.faces(">Z").workplane().rect(frame_width - 2*wall_thickness, frame_height - 2*wall_thickness).cutBlind(-thickness)

# Add Chamfers to the inner left corners of the hole
# We select vertical edges inside the hole that are on the left side (X < 0)
# This mimics the shape shown in the image where the wall thickens near the point.
result = result.edges("|Z and <X").chamfer(15.0)


# 3. Add Tabs (Top and Bottom)
# Two tabs on top, two on bottom.
# Top Tabs
for x_pos in [-tab_spacing/2, tab_spacing/2]:
    # Top
    result = result.faces(">Y").workplane(centerOption="CenterOfBoundBox") \
        .center(x_pos, 0) \
        .rect(tab_width, thickness) \
        .extrude(tab_height)
    
    # Bottom
    result = result.faces("<Y").workplane(centerOption="CenterOfBoundBox") \
        .center(x_pos, 0) \
        .rect(tab_width, thickness) \
        .extrude(tab_height)

# 4. Add Holes
# Hole through the pointed left side (Y-axis cylinder roughly, or perpendicular to face?)
# The image shows a hole going through the "point" section. It looks perpendicular to the angled face
# or just along the Y axis? Given the side hole on the right is perpendicular to the face...
# Let's look at the left hole. It looks like it goes through the thickness (Z axis) ??
# No, the main extrusion is Z. The hole is in the "face" of the point. 
# Looking at the shading, the hole is on the angled face.
# Wait, looking at the "Side" hole on the right vertical face. It goes into the thickness.
# So the holes are perpendicular to the outer perimeter faces.

# Right side hole
result = (
    result.faces(">X").workplane()
    .hole(side_hole_diameter, depth=wall_thickness + 5) # Cut through the wall
)

# Left side hole (on the point)
# This is tricky because the face is angled.
# We create a workplane on the angled face(s). 
# Or, simpler: create a cylinder and cut it.
# The hole seems to be right at the tip. 
# It looks like it passes through the tip along the X axis?
# No, looking at the cylinder inside, it looks perpendicular to the angled face.
# Let's assume it's just a hole through the tip, probably for a pin.
# Most likely simpler: A hole along the Z axis (thickness) at the point? 
# The image perspective is isometric. The top tabs go UP (Z or Y?).
# Let's re-orient. 
# The initial extrusion was Z. So the front face is XY.
# Tabs are on top/bottom faces (+Y, -Y).
# The pointy part is -X.
# The hole on the right (+X) face goes through the wall (along -X).
# The hole on the left (point) face looks like it goes through the wall (perpendicular to angle).

# Let's create a plane for the angled face.
# The angled face is defined by (-half_w, half_h) and (point_x, 0).
# We can select it using a selector.
# We need to cut a hole in both angled faces or just the tip?
# It looks like one hole right near the tip. 
# Let's assume the hole is horizontal (Y-axis aligned) passing through the point structure?
# Or perpendicular to the face. Let's do perpendicular to the face.

# Find the angled face on the "top-left" quadrant
angled_face = result.faces("<X").faces(">Y").val() # Upper angled face
# This selector might be fragile. 
# Let's try a different approach: Cut a cylinder through the point.
# It looks like a single hole located near the tip.
# Let's put it on the tip, extending inward.
# Given the symmetry, maybe it's a hole through the X-axis at the tip?
# Let's look at the shadow inside the hole. It looks cylindrical.
# Let's place a hole on the tip face (which is technically a vertice, but in reality might be a small flat or just the intersection).
# Let's drill a hole perpendicular to the angled surface.

# Let's select the upper angled face.
result = (
    result.faces("<X").faces(">Y") # Select upper left angled face
    .workplane(centerOption="CenterOfMass")
    .hole(point_hole_diameter)
)

# Wait, the image shows a hole on the *lower* angled face too? Or is it symmetric?
# It looks like a single hole on the angled face visible to camera.
# And a hole on the flat right face.
# Actually, looking at the right hole, it sits in a recessed area? No, that's just the inner chamfer/angle seen through the hole.
# The right hole is definitely on the flat face.

# Let's add the hole to the bottom angled face for symmetry, though hidden in view.
result = (
    result.faces("<X").faces("<Y") # Select lower left angled face
    .workplane(centerOption="CenterOfMass")
    .hole(point_hole_diameter)
)

# Refinement: The image shows the hole on the left is on the *vertical* face of the point?
# If the point was flattened?
# No, the point is sharp.
# Let's assume the hole is simply drilled through the X-axis near the tip.
# This produces an elliptical hole on the angled face, which matches the image somewhat.
# Let's try that. It's cleaner mechanically.
result = result.faces("<X").faces(">Y").cut(
    cq.Workplane("YZ").center(0, 0).circle(point_hole_diameter/2).extrude(100)
)
# That would cut a weird shape.
# Let's revert to "Normal to Face" hole on the angled faces.
# The previous code block `result.faces("<X").faces(">Y").workplane(...).hole(...)` does exactly that.

# Let's clean up the order to ensure `result` is consistent.
# Re-running the logic cleanly.

# --- Final Clean Construction Script ---

# 1. Main body
r = (
    cq.Workplane("XY")
    .moveTo(half_w, half_h)
    .lineTo(half_w, -half_h)
    .lineTo(-half_w, -half_h)
    .lineTo(point_x, 0)
    .lineTo(-half_w, half_h)
    .close()
    .extrude(thickness)
)

# 2. Cutout
# Rectangle
r = r.faces(">Z").workplane().rect(frame_width - 2*wall_thickness, frame_height - 2*wall_thickness).cutBlind(-thickness)
# Chamfer inner vertical edges on the left side to follow the outer point shape
r = r.edges("|Z and <X").chamfer(15.0)

# 3. Tabs
# Top
r = r.faces(">Y").workplane(centerOption="CenterOfBoundBox") \
    .center(-tab_spacing/2, 0).rect(tab_width, thickness).extrude(tab_height) \
    .faces(">Y").workplane(centerOption="CenterOfBoundBox") \
    .center(tab_spacing, 0).rect(tab_width, thickness).extrude(tab_height) # Shift relative to prev workplane? No, workplane stack.

# Better tab logic
def add_tabs(shape, face_selector):
    return (
        shape.faces(face_selector).workplane(centerOption="CenterOfBoundBox")
        .transformed(offset=(0, 0, 0)) # Ensure local coords
        .center(-tab_spacing/2, 0).rect(tab_width, thickness).extrude(tab_height)
        .faces(face_selector).workplane(centerOption="CenterOfBoundBox")
        .center(tab_spacing/2, 0).rect(tab_width, thickness).extrude(tab_height)
    )

# Re-do tabs simply
# Top tabs
r = r.faces(">Y").workplane(centerOption="CenterOfBoundBox") \
    .pushPoints([(-tab_spacing/2, 0), (tab_spacing/2, 0)]) \
    .rect(tab_width, thickness) \
    .extrude(tab_height)

# Bottom tabs
r = r.faces("<Y").workplane(centerOption="CenterOfBoundBox") \
    .pushPoints([(-tab_spacing/2, 0), (tab_spacing/2, 0)]) \
    .rect(tab_width, thickness) \
    .extrude(tab_height)

# 4. Holes
# Right side hole
r = r.faces(">X").workplane().center(0, 0).hole(side_hole_diameter, depth=wall_thickness + 2)

# Point hole
# Based on the image, there is a hole on the angled face.
# We will place it midway on the angled face.
r = r.faces("<X").faces(">Y").workplane(centerOption="CenterOfMass").hole(point_hole_diameter, depth=20)
# Mirror hole on bottom angled face for good measure? The image doesn't show it but it's likely.
# Just the top one is visible.

result = r