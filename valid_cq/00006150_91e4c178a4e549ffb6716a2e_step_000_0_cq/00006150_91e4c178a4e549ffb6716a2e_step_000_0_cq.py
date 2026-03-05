import cadquery as cq

# Parametric dimensions
# Overall dimensions
overall_length = 50.0  # Length along the long axis
overall_width = 40.0   # Width of the widest part
total_height = 15.0    # Total thickness/height

# Dimensions for the "cutout" or steps
# It looks like a central T-shape or a block with side steps removed.
# Let's model it as a base rectangle with two corner cutouts or a T-shape profile extruded.

# Looking at the image:
# There is a wider top section (let's call it the "head") and a narrower bottom section (the "body").
# Or, if oriented flat, a wider central section and narrower ends? 
# No, it looks like a T-slot nut shape.
# There is a wide upper part and a narrower lower part.
# Let's assume standard orientation for such a part: 
# The top face shows a "T" shape if viewed from the side, but here we see a "T" shape in the cross-section.

# Let's interpret the geometry based on the isometric view:
# It looks like a rectangular block with two rectangular notches cut out of the corners on one long side.
# OR, it's a T-shaped extrusion.
# Let's assume it's a T-shape block.

# Width of the top wide part (the "flange")
head_width = 40.0
# Width of the bottom narrow part (the "web")
web_width = 20.0 

# Length of the entire piece
length = 60.0

# Height of the bottom part
web_height = 10.0
# Height of the top part (flange thickness)
head_height = 10.0

# Total height is sum
total_height = web_height + head_height

# Let's refine the model strategy.
# Create a sketch on the XY plane that represents the T-profile and extrude it.
# Or create two boxes and union them.

# Approach: Union of two boxes to form the T-shape.
# Box 1: The wide top part (the flange)
# Box 2: The narrow bottom part (the web)

# Let's adjust dimensions to match the visual proportions better.
# The object looks somewhat square-ish in overall footprint.
L = 40.0  # Length
W_wide = 30.0 # Width of the wide top section
W_narrow = 15.0 # Width of the narrow bottom section
H_wide = 8.0  # Height (thickness) of the top section
H_narrow = 8.0 # Height of the bottom section

# Looking closely at the image again.
# It actually looks like two side blocks attached to a central block, but the top surface is flat and continuous.
# This is a classic "T-slot nut" shape inverted, or simply a stepped block.
# Let's model it as a base block with a wider block on top.

# Final Dimensions estimation:
# Length (depth into the page): 50
# Width (widest dimension): 40
# Width (narrowest dimension): 20
# Height (bottom section): 10
# Height (top section): 10

# Create the bottom narrow box
# Centered on X and Y for symmetry
bottom_block = cq.Workplane("XY").box(20, 50, 10)

# Create the top wide box
# We need to position it on top of the bottom block.
# The bottom block is 10mm high, centered at Z=0, so its top face is at Z=5.
# We want to place the next block on top of that.
# Alternatively, we can just position the centers.

# Improved Dimension set for visual accuracy
length = 50.0      # Dimension along the axis that goes into the distance
width_wide = 40.0  # The full width of the top plate
width_narrow = 20.0 # The width of the rectangular block underneath
height_wide = 10.0 # Thickness of the top plate
height_narrow = 10.0 # Height of the bottom block

# Strategy:
# 1. Create the wide top plate.
# 2. Create the narrow bottom block.
# 3. Union them.

# Center everything
# Top plate
top_plate = cq.Workplane("XY").box(width_wide, length, height_wide)

# Bottom block
# Position: it needs to be below the top plate.
# Top plate is centered at Z=0 (height from -5 to 5).
# Bottom block needs to be attached to the bottom face (Z=-5).
# Bottom block height is 10. Center of bottom block will be at -5 - (10/2) = -10.
bottom_block = cq.Workplane("XY").workplane(offset=- (height_wide/2 + height_narrow/2)).box(width_narrow, length, height_narrow)

# Combine
result = top_plate.union(bottom_block)

# Let's rotate it to match the isometric view roughly
# The image shows the wide part on top? No, wait.
# The image shows a block where the wider part is "up" relative to the "web". 
# Actually, let's look at the shadows and perspective.
# We see a top face that is a large rectangle.
# We see a side face (front-left) showing the step profile.
# The step profile consists of a vertical line, a horizontal step in, and another vertical line.
# This confirms it's a T-shape. The wide part is on top.

# Let's re-verify the axes. 
# Usually Z is up.
# The top surface is the large rectangle (width_wide x length).
# The "step" is visible on the front face.

# Let's construct it as a single extrusion of the T-profile for cleaner code.
# The profile is on the Front plane (XZ or YZ depending on orientation preference).
# Let's draw the T-shape on the XZ plane and extrude along Y.

L_extrude = 50.0
W_top = 40.0
H_top = 10.0
W_bot = 20.0
H_bot = 12.0

result = (
    cq.Workplane("XZ")
    .moveTo(-W_top/2, H_bot + H_top) # Start top-left corner
    .lineTo(W_top/2, H_bot + H_top)  # Top edge
    .lineTo(W_top/2, H_bot)          # Top-right vertical down
    .lineTo(W_bot/2, H_bot)          # Step in right
    .lineTo(W_bot/2, 0)              # Bottom vertical right
    .lineTo(-W_bot/2, 0)             # Bottom edge
    .lineTo(-W_bot/2, H_bot)         # Bottom vertical left
    .lineTo(-W_top/2, H_bot)         # Step out left
    .close()
    .extrude(L_extrude)
)

# The extrusion centers the shape in the Y direction by default? 
# No, extrude(distance) goes in the positive normal direction usually.
# To match the view, we might want to center it or just leave it. 
# Let's center the extrusion for good practice.
result = (
    cq.Workplane("XY") # Drawing on XY plane, extruding up Z is standard, but let's stick to the profile approach or simple box union.
    # Box union is often easier to read.
)

# Re-doing with box union approach for clarity and guaranteed validity.
# Let's orient it so the wide face is facing +Z (Top).

full_length = 60.0
wide_width = 40.0
narrow_width = 20.0
top_thickness = 10.0
bottom_height = 10.0

# Base (narrow part)
base = cq.Workplane("XY").box(full_length, narrow_width, bottom_height)

# Top (wide part)
# We need to shift the workplane to the top of the base
top = (
    base.faces(">Z")
    .workplane()
    .box(full_length, wide_width, top_thickness)
)

# The image shows the object oriented such that the long dimension is along X or Y.
# Let's adjust dimensions to match the image proportions. 
# The image shows the object is longer than it is wide.
# Let's say Length=60, Width=40.
# The "step" cuts into the width.
# So we have a 60x40 block on top of a 60x20 block.

# Create the result
result = top
