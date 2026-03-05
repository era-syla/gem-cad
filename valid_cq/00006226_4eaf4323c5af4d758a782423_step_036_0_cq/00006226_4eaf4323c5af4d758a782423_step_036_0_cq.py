import cadquery as cq

# Parametric dimensions
length = 100.0   # Length of the longer wall
width = 60.0     # Length of the shorter wall (width of the assembly)
height = 40.0    # Height of the walls
thickness = 5.0  # Thickness of the walls and base
base_depth = 40.0 # Depth of the horizontal base plate

# Create the L-shape profile for the walls
# Strategy: Create a sketch on the XY plane and extrude it up
# The L-shape consists of two rectangles joined at a corner

# Method 1: Boolean construction
# Create the first wall (along X)
wall1 = cq.Workplane("XY").box(length, thickness, height, centered=(False, False, False))

# Create the second wall (along Y)
# We offset it so the corner meets nicely
wall2 = cq.Workplane("XY").workplane(offset=0).moveTo(0, 0).box(thickness, width, height, centered=(False, False, False))

# Union the two walls
walls = wall1.union(wall2)

# Create the base plate
# It sits "inside" the corner.
# Dimensions: X = length - thickness (if aligned with wall1 internal face), 
#             Y = base_depth
#             Z = thickness (it's a floor)
# Let's align it carefully based on the visual.
# It looks like the base fills the corner formed by the walls.

base = (cq.Workplane("XY")
        .workplane(offset=height/2 - height/2) # Start at Z=0
        .moveTo(thickness, thickness)          # Start from the inner corner
        .box(length - thickness, base_depth - thickness, thickness, centered=(False, False, False))
       )

# However, looking closer at the image, the geometry is simpler:
# It looks like an extruded "U" or "J" profile, or simply two walls meeting with a floor between them.
# Let's rebuild it as a single shell or additive box approach for cleaner parametric behavior.

# Revised Parametric approach:
# 1. Create a large base block.
# 2. Shell it? No, walls might have different heights.
# 3. Additive boxes is the safest and most readable way.

# Re-defining dimensions to be clearer based on the visual proportions
L_wall_length = 80.0
L_wall_height = 40.0
S_wall_length = 50.0 # This is the "depth" of the L-shape
wall_thickness = 4.0

# Construction
# 1. Main Long Wall (Front/Right in isometric view)
long_wall = cq.Workplane("XY").box(L_wall_length, wall_thickness, L_wall_height)

# 2. Short Wall (Left/Back in isometric view)
# Positioned at the end of the long wall
short_wall = (cq.Workplane("XY")
              .translate((-L_wall_length/2 + wall_thickness/2, S_wall_length/2 - wall_thickness/2, 0))
              .box(wall_thickness, S_wall_length, L_wall_height)
             )

# 3. The Floor/Base
# It connects the two walls at the bottom.
# It seems to extend from the inner corner.
# Visual check: The floor seems to align with the top of the short wall's extension?
# No, looking at the image, the floor is at the *top* of the volume shown? 
# Wait, let's look at the shading. 
# The vertical faces are grey. The horizontal face is lighter grey.
# The geometry looks like two vertical walls meeting at a 90-degree corner, 
# and a horizontal shelf connecting them, situated somewhere along the height or at the bottom?
# Actually, it looks like a simple L-bracket corner with a bottom floor.
# Or potentially a "corner shelf". Let's assume the standard orientation: Z is up.
# Walls are vertical. There is a horizontal plate.
# The horizontal plate appears to be at the *middle* or simply at the bottom (inverted view?).
# Let's assume standard view: Walls are going UP. The flat plate is at the BOTTOM.
# Or... is the flat plate at the TOP?
# If the flat plate is at the top, the walls are going DOWN.
# Let's assume the standard: Base plate at Z=0, Walls going Z+.
# BUT, looking at the junction, the walls go UP, and there is a horizontal surface.
# The horizontal surface is positioned roughly in the middle of the vertical extent? 
# No, checking the corners, it looks like a single solid object, like a tray corner.
# Let's stick to the Additive approach.

# Final Plan:
# - Wall 1 (Long)
# - Wall 2 (Short)
# - Base Plate (filling the void)

result = (
    cq.Workplane("XY")
    # Base Plate
    .box(L_wall_length, S_wall_length, wall_thickness)
    # Move to top face of base to start walls
    .faces(">Z").workplane()
    # Create the L-shaped wall profile
    # Draw outer rectangle
    .rect(L_wall_length, S_wall_length)
    # Draw inner rectangle to subtract (creating the wall thickness)
    .rect(L_wall_length - 2*wall_thickness, S_wall_length - 2*wall_thickness)
    # Extrude walls up
    .extrude(L_wall_height - wall_thickness)
    # Now cut away the two "open" sides to form the specific corner shape in the image
    # The image shows two walls forming a corner, not a 4-wall box.
    # We need to remove the "front" and "right" (relative to the corner) sections.
)

# Alternative cleaner construction for the specific "Corner" shape:
# 1. Back Wall
# 2. Side Wall
# 3. Floor connecting them

final_L_length = 60.0
final_W_depth = 40.0
final_H_height = 30.0
final_thickness = 2.0

# 1. Base rectangle (The floor)
base = cq.Workplane("XY").box(final_L_length, final_W_depth, final_thickness)

# 2. Back Wall (along the long edge)
back_wall = (
    cq.Workplane("XY")
    .translate((0, final_W_depth/2 - final_thickness/2, final_H_height/2 - final_thickness/2))
    .box(final_L_length, final_thickness, final_H_height)
)

# 3. Side Wall (along the short edge)
side_wall = (
    cq.Workplane("XY")
    .translate((-final_L_length/2 + final_thickness/2, 0, final_H_height/2 - final_thickness/2))
    .box(final_thickness, final_W_depth, final_H_height)
)

# The image shows the floor doesn't extend past the walls? 
# Actually, the image shows an L-shaped extrusion profile (a corner) with a floor inserted.
# Let's refine the positioning so corners are flush.

result = (
    cq.Workplane("XY")
    # Create the Side Wall (Left in image)
    .box(final_thickness, final_W_depth, final_H_height, centered=(True, True, False))
    # Move to create the Back Wall (Right in image), merging unions
    .union(
        cq.Workplane("XY")
        .moveTo(final_L_length/2 - final_thickness/2, -final_W_depth/2 + final_thickness/2)
        .box(final_L_length, final_thickness, final_H_height, centered=(True, True, False))
    )
    # Create the Floor
    # The floor sits inside the L-shape
    .union(
        cq.Workplane("XY")
        .moveTo(final_L_length/2, 0) # Adjust center
        .box(final_L_length - final_thickness, final_W_depth - final_thickness, final_thickness, centered=(True, True, False))
        .translate((0, -final_thickness/2, 0)) # Minor adjustment to align with inner faces
    )
)

# Let's try a much simpler sketch-and-extrude approach for guaranteed correctness.
# The object is an "L" shape in the Top View, extruded up, then shelled?
# No, it's a corner wall with a floor.

# Precise construction based on origin at the outer corner vertex:
L = 60.0 # Length along X
W = 40.0 # Length along Y
H = 30.0 # Height Z
T = 3.0  # Thickness

result = (
    cq.Workplane("XY")
    # 1. Draw the floor profile (a rectangle)
    .rect(L, W, centered=False)
    .extrude(T)
    # 2. Select the top face of the floor
    .faces(">Z").workplane()
    # 3. Draw the wall profiles on top of the floor
    # We want walls along the X axis (at Y=W) and Y axis (at X=0)?
    # Let's look at image: It's a corner. Let's put the corner at Origin (0,0).
    # Wall 1: Along X axis.
    # Wall 2: Along Y axis.
    .rect(T, W, centered=False) # Wall along Y axis (at X=0)
    .extrude(H - T)
    .faces(">Z").workplane(offset=-(H-T)) # Go back to floor level
    .moveTo(0, W-T)
    .rect(L, T, centered=False) # Wall along X axis (at Y=W-T roughly)
    .extrude(H - T)
    # Combine everything
    .combine()
)

# Re-orienting to match the isometric view of the image perfectly.
# In the image, the corner is closest to the viewer.
# Left wall goes "back-left", Right wall goes "back-right".
# Floor is between them.

res_L = 50.0
res_W = 40.0
res_H = 30.0
res_T = 3.0

result = (
    cq.Workplane("XY")
    # Base Floor
    .box(res_L, res_W, res_T, centered=(False, False, False))
    
    # Left Wall (Side)
    .faces(">Z").workplane()
    .moveTo(0, 0)
    .rect(res_T, res_W, centered=(False, False))
    .extrude(res_H)
    
    # Right Wall (Front/Back)
    .faces(">Z").workplane(offset=-res_H) # Reset to top of floor
    .moveTo(0, 0)
    .rect(res_L, res_T, centered=(False, False))
    .extrude(res_H)
    
    # Union is implicit in recent CQ versions with extrude on workplane, 
    # but explicit combine ensures solid
    .combine()
)