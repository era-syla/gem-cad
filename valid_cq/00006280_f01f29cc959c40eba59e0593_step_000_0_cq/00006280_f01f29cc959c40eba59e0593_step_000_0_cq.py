import cadquery as cq

# Parametric dimensions
length = 80.0
height = 12.0
thickness = 2.0
chamfer_size = 2.0
clip_length = 3.0
clip_depth = 1.5
clip_thickness = 1.0

# Create the main rectangular body
main_body = (
    cq.Workplane("XY")
    .box(length, height, thickness)
)

# Apply chamfers to the four corners of the main face (Z-axis)
# We select edges parallel to the Z axis and then filter for the corners
# Alternatively, we can construct the 2D sketch with chamfers first. Let's do the sketch approach for cleaner geometry.

# Create the profile with chamfered corners
pts = [
    (length/2 - chamfer_size, height/2), # Top Right (start of chamfer)
    (length/2, height/2 - chamfer_size), # Right Top
    (length/2, -height/2 + chamfer_size), # Right Bottom
    (length/2 - chamfer_size, -height/2), # Bottom Right
    (-length/2 + chamfer_size, -height/2), # Bottom Left
    (-length/2, -height/2 + chamfer_size), # Left Bottom
    (-length/2, height/2 - chamfer_size), # Left Top
    (-length/2 + chamfer_size, height/2), # Top Left
]

base_plate = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(thickness)
)

# Create the clip/hook geometry on the left end
# Looking at the image, there are two small prongs or hooks sticking out from the back face on the left side
# Let's model them as an extrusion from the back face (negative Z)

# Define the hook profile
hook_width = 1.5
hook_gap = 3.0 # Distance between the two hooks or vertical positioning
hook_stickout = 3.0 # How far they stick out in Z
hook_catch = 0.5 # The little tooth part

# We will position the hooks relative to the left edge (-length/2)
# Creating a sketch on the YZ plane (side view) located at the left end
left_face_x = -length/2

# Helper function to create a single hook shape
def create_hook(y_pos):
    hook = (
        cq.Workplane("YZ")
        .workplane(offset=left_face_x + 1.0) # Slightly inset from the very edge or right on it. Image shows flush.
        .center(0, y_pos) # Z is horizontal here (thickness), Y is vertical (height)
        .polyline([
            (0, 0),
            (hook_stickout, 0),
            (hook_stickout, -hook_catch), # The catch pointing down/in
            (hook_stickout - hook_catch, -hook_catch),
            (0, -hook_width) # Taper back to base
        ])
        .close()
        .extrude(1.0) # Width of the hook along X axis
    )
    return hook

# Create hooks. Based on the image, they are on the back side.
# Let's attach them to the back face.
# The image shows the hooks near the left edge.
# Instead of complex sketches, let's just draw rectangles on the back and extrude/cut.

# Re-evaluating the image:
# It looks like there are two small tabs protruding from the *back* face (-Z), near the left edge (-X).
# They look like simple snap-fit cantilevers.

hook_sketch = (
    cq.Workplane("XZ") # Looking from top/bottom
    .workplane(offset=height/2) # Move to top edge
    # This orientation is tricky. Let's stick to the main coordinate system.
)

# Let's model the hooks by adding material to the back face
# Back face is at z = 0 (if we extruded up) or z = -thickness/2 depending on origin.
# Our base_plate is centered on Z=0? No, .extrude(thickness) goes from Z=0 to Z=thickness.
# So back face is Z=0.

# Hook Parameters
hook_x_offset = -length/2 + 2.0 # Position from left edge
hook_z_height = 2.5 # How tall the hook stands from the back face
hook_thickness_y = 1.5 # Thickness of the hook walls
hook_tip_overhang = 0.5

# Top Hook
top_hook = (
    cq.Workplane("XY")
    .workplane(offset=0) # Back face (bottom of extrusion)
    .center(hook_x_offset, height/2 - 2.0) # Position near top corner
    .rect(1.5, hook_thickness_y)
    .extrude(-hook_z_height) # Extrude downwards (negative Z)
)

# Add the 'catch' to the top hook
top_hook_catch = (
    cq.Workplane("XY")
    .workplane(offset=-hook_z_height)
    .center(hook_x_offset, height/2 - 2.0) # Same center
    .rect(1.5, hook_thickness_y)
    .workplane(offset=0.5) # small tip section
    .center(0, -0.3) # Shift for the catch
    .rect(1.5, hook_thickness_y)
    .loft()
)
# That's getting complicated. Let's do a simple extrusion of a profile on the XZ plane.

# Final approach for hooks: Draw profile on side (XZ plane at specific Y offsets)
# The image shows two hooks, one near top, one near bottom.
hook_profile_pts = [
    (0, 0),
    (0, -2.5), # Stick out
    (0.5, -3.0), # Tip point
    (1.5, -2.5), # Back angle
    (1.5, 0)
]

# Create the hook geometry
hooks = (
    cq.Workplane("XZ")
    .workplane(offset=height/2 - 2.0) # Top hook Y position
    .center(hook_x_offset, 0)
    .polyline(hook_profile_pts).close()
    .extrude(hook_thickness_y) # Extrude in Y
    # Mirror or create second hook
    .workplane(offset=-(height - 4.0 + hook_thickness_y)) # Move to bottom hook position
    .center(0, 0) # Reset local center if needed, but polyline uses relative coords usually? No, absolute.
    .polyline(hook_profile_pts).close()
    .extrude(hook_thickness_y)
)

# Combine geometry
result = base_plate.union(hooks)

# Refine based on specific visual cues in the image
# The image actually shows the hooks are aligned with the chamfer or slightly inset.
# The hooks seem to be "L" shaped clips.
# Let's refine the hook shape to be simpler and match the "clip" aesthetic more closely.

result = (
    cq.Workplane("XY")
    # Base Shape
    .moveTo(length/2 - chamfer_size, height/2)
    .lineTo(length/2, height/2 - chamfer_size)
    .lineTo(length/2, -height/2 + chamfer_size)
    .lineTo(length/2 - chamfer_size, -height/2)
    .lineTo(-length/2 + chamfer_size, -height/2)
    .lineTo(-length/2, -height/2 + chamfer_size)
    .lineTo(-length/2, height/2 - chamfer_size)
    .lineTo(-length/2 + chamfer_size, height/2)
    .close()
    .extrude(thickness)
)

# Add the clips to the back (negative Z)
clip_y_spacing = height - 4.0 # Distance between outer edges of clips
clip_width = 1.2
clip_stickout = 2.5
clip_x_pos = -length/2 + 1.0 # Near left edge

# Upper Clip
clip1 = (
    cq.Workplane("XZ")
    .workplane(offset=height/2 - 1.5) # Y Position
    .moveTo(clip_x_pos, 0)
    .lineTo(clip_x_pos, -clip_stickout)
    .lineTo(clip_x_pos + 0.5, -clip_stickout - 0.5) # Angled tip
    .lineTo(clip_x_pos + 1.5, -clip_stickout) 
    .lineTo(clip_x_pos + 1.5, 0)
    .close()
    .extrude(clip_width)
)

# Lower Clip
clip2 = (
    cq.Workplane("XZ")
    .workplane(offset=-(height/2 - 1.5) - clip_width) # Y Position (mirrored essentially)
    .moveTo(clip_x_pos, 0)
    .lineTo(clip_x_pos, -clip_stickout)
    .lineTo(clip_x_pos + 0.5, -clip_stickout - 0.5) # Angled tip
    .lineTo(clip_x_pos + 1.5, -clip_stickout) 
    .lineTo(clip_x_pos + 1.5, 0)
    .close()
    .extrude(clip_width)
)

result = result.union(clip1).union(clip2)