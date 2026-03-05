import cadquery as cq

# Parameters for dimensions
box_length = 100.0
box_width = 100.0
box_height = 100.0
wall_thickness = 10.0
groove_radius = 2.0  # Radius of the vertical groove
groove_offset = 30.0 # Distance from the left edge of the front face

# 1. Create the base outer box
# We create a solid box first
base_box = cq.Workplane("XY").box(box_length, box_width, box_height)

# 2. Hollow out the box to create the frame structure
# The image shows open faces on the top, right, and bottom (implied by symmetry or common frame logic, but let's stick to visible).
# Actually, looking at the image:
# - Top is open (framed)
# - Right is open (framed)
# - Front is solid plate? No, looking closely at the front face, it's a solid wall with a groove.
# - Left is a solid wall.
# - Back is a solid wall.
# Let's re-evaluate. It looks more like a 5-sided box (open top? no, open right? no).
# Let's interpret it as a hollow shell where specific faces are cut out.
# Visible features:
# - A main cubic volume.
# - Shell thickness applies.
# - Top face has a large rectangular cutout, leaving a rim.
# - Right face has a large rectangular cutout, leaving a rim.
# - Front face is solid but has a vertical semi-circular groove running top to bottom.
# - Left face appears solid.
# - Back face appears solid.
# - Bottom face appears to have a cutout similar to the top and right (we can see through the right face to the bottom rim).

# Strategy:
# 1. Make a solid box.
# 2. Shell it (hollow it out) with openings on specific faces?
#    Or simpler: Make a hollow box by subtracting a smaller box, then cut holes.
#    Let's go with: Create solid block -> Shell it -> Cut windows.

# Create the main solid block
part = cq.Workplane("XY").box(box_length, box_width, box_height)

# Create the inner cutout to make it a hollow container with walls on all sides
# We'll subtract a smaller box from the inside.
inner_box = (
    cq.Workplane("XY")
    .box(box_length - 2*wall_thickness, 
         box_width - 2*wall_thickness, 
         box_height - 2*wall_thickness)
)
part = part.cut(inner_box)

# Now we have a closed hollow box with walls of `wall_thickness`.
# We need to open up the Top, Right, and Bottom faces as seen in the image.
# The image shows a "frame-like" structure on the right and top.

# Cutout for the Top face
# Select top face, draw rectangle, cut through the wall
part = (
    part.faces(">Z")
    .workplane()
    .rect(box_length - 2*wall_thickness, box_width - 2*wall_thickness)
    .cutThruAll() 
)

# Cutout for the Bottom face (visible through the side)
# Since cutThruAll on the top might have already cut the bottom if we aren't careful,
# but cutThruAll typically cuts everything in the projection. 
# If the previous cut went through both top and bottom walls, we are good.
# Let's verify. A box has top and bottom walls. If I select top face and cut thru all, it punches through top and bottom.
# This matches the "frame" look where you can see through top-to-bottom.

# Cutout for the Right face
part = (
    part.faces(">X")
    .workplane()
    .rect(box_width - 2*wall_thickness, box_height - 2*wall_thickness)
    .cutThruAll() # This will cut right and left walls if we aren't careful.
)

# Wait, the Left face in the image (the one facing -X, if Right is +X) looks SOLID.
# The Front face is solid (with groove).
# The Back face looks solid.
# So we should NOT use cutThruAll for the side cut, as it would remove the Left wall.
# We should cut blind with a depth equal to the wall thickness + a small tolerance, or just up to the inner void.

# Re-doing the cuts more precisely to preserve opposite walls where needed.

# Reset strategy:
# 1. Base Box
# 2. Hollow out completely (shell) but keep faces? No, simple booleans are easier to reason about.

# Step 1: Outer Solid
result = cq.Workplane("XY").box(box_length, box_width, box_height)

# Step 2: Inner Void (making it a hollow box with 6 walls)
inner_void = cq.Workplane("XY").box(
    box_length - 2*wall_thickness, 
    box_width - 2*wall_thickness, 
    box_height - 2*wall_thickness
)
result = result.cut(inner_void)

# Step 3: Open the Top and Bottom faces
# This effectively removes the material in the center of the top and bottom plates.
# Visible in image: Top is open. Bottom rim suggests bottom is open.
cutout_top_bottom = cq.Workplane("XY").box(
    box_length - 2*wall_thickness, 
    box_width - 2*wall_thickness, 
    box_height + 10.0 # Make it taller to cut through
)
result = result.cut(cutout_top_bottom)

# Step 4: Open the Right face ONLY
# The Left face (-X) remains solid.
# We place a cutting box on the right side.
cutout_right = (
    cq.Workplane("YZ")
    .workplane(offset=box_length/2.0) # Move to Right face plane
    .rect(box_width - 2*wall_thickness, box_height - 2*wall_thickness)
    .extrude(-wall_thickness - 1.0) # Cut into the box, slightly deeper than wall
)
result = result.cut(cutout_right)

# Step 5: Add the vertical groove on the Front face
# The front face corresponds to -Y in standard "box" creation (Front/Back are Y, Left/Right are X, Top/Bottom are Z usually).
# In the image, let's assume:
# - Right Face (+X) is the open frame on the right.
# - Top Face (+Z) is the open frame on top.
# - Front Face (-Y) is the solid face facing us.
# - Left Face (-X) is the solid face on the left.

# The groove is on the Front Face (-Y).
# It runs vertically (along Z).
# It is offset from the corner. 
# In the image, the groove is on the Front face, near the edge shared with the Left face.

# Select the Front Face (-Y)
# We need to cut a semi-circular channel.
groove = (
    result.faces("<Y").workplane()
    # Move the origin to the center of the face, so (0,0) is center.
    # The face is on the XZ plane roughly.
    # We want the groove offset from the left edge of this face.
    # Left edge of front face corresponds to X = -box_length/2.
    .transformed(offset=cq.Vector(-box_length/2.0 + groove_offset, 0, 0))
    .circle(groove_radius)
    .cutThruAll() # Cut through the wall thickness
)

# However, a simple cutThruAll with a circle on the face will make a hole, not a groove,
# unless we extrude it along the Z axis.
# The `cutThruAll` on a 2D circle usually implies cutting normal to the sketch plane (Y axis here).
# That would make a hole through the front wall.
# The image shows a vertical GROOVE running top to bottom.
# So we sketch on the top face or draw a cylinder to subtract.

# Better groove approach: Create a cylinder and subtract it.
# Position:
# X: -box_length/2 + groove_offset
# Y: -box_width/2 (center of the front wall thickness)
# Z: Center (0)
# Height: box_height
groove_cylinder = (
    cq.Workplane("XY")
    .workplane(offset=-box_width/2) # Move to front face plane roughly
    .moveTo(-box_length/2 + groove_offset, 0)
    .circle(groove_radius)
    .extrude(box_height) # This extrudes in Z? No, Workplane("XY") extrudes in Z.
)
# Wait, let's just place a cylinder explicitly.
groove_cutter = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(-box_length/2 + groove_offset, -box_width/2, 0))
    .circle(groove_radius)
    .extrude(box_height, both=True) # Extrude up and down to cover full height
)

# We want the groove to be "embedded" in the face. 
# Looking at the image, it looks like a half-round cut or a full slot cut into the face.
# It seems to go slightly into the thickness.
# If we center the cylinder exactly on the face surface (-box_width/2), it cuts a half-circle groove.
# Let's adjust depth if necessary, but centering on the face plane is a standard "groove" look.

result = result.cut(groove_cutter)