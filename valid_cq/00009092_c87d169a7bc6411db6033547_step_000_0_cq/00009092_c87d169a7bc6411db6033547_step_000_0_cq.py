import cadquery as cq

# --- Parametric Dimensions ---
length = 100.0       # Overall length of the tray
width = 60.0         # Overall width of the tray
height = 10.0        # Total height of the tray
wall_thickness = 5.0 # Thickness of the side walls
floor_thickness = 2.0 # Thickness of the bottom floor

# Groove/Slot details
slot_depth = 2.0     # Depth of the cutout on the top edge
slot_width = 3.0     # Width of the cutout on the top edge
corner_radius = 2.0  # Fillet radius for the outer corners

# --- Modeling Process ---

# 1. Create the main block (the outer envelope)
# We center it on X and Y, but keep Z at 0 for the base
base = cq.Workplane("XY").box(length, width, height)

# 2. Hollow out the inside to create the tray
# We select the top face and shell inwards. 
# Alternatively, we can cut a pocket. A pocket is often more robust for specific floor thickness control.
# Let's use a cut for explicit control.
inner_length = length - (2 * wall_thickness)
inner_width = width - (2 * wall_thickness)
cut_depth = height - floor_thickness

tray = (base.faces(">Z")
        .workplane()
        .rect(inner_length, inner_width)
        .cutBlind(-cut_depth))

# 3. Create the small notches/grooves on the top rim
# Looking at the image, there are notches on the shorter sides (width-wise).
# They appear to be centered or symmetric. Let's assume there are two notches on each short side.
# However, looking closer, it looks like there are notches on the *long* sides, near the ends.
# Actually, looking at the orientation, the "length" is the longer dimension. The notches are on the long walls.
# Let's re-examine the image. It's a rectangular tray. The side walls have small rectangular cutouts on the top face.
# There appear to be two notches on the visible long side.
# Let's place notches on the top face of the rim.

# Define notch positions relative to center
notch_offset_x = length/2 - wall_thickness - 5 # Position near the ends

# Select the top face
top_face = tray.faces(">Z").workplane()

# Cut notches on the positive Y side wall
result_with_notches = (top_face
                       # Notch 1 (Right side in image, +X)
                       .moveTo(length/2 - 15, width/2 - wall_thickness/2)
                       .rect(slot_width, wall_thickness + 2) # +2 to ensure clean cut through edge
                       .cutBlind(-slot_depth)
                       
                       # Notch 2 (Left side in image, -X)
                       .moveTo(-(length/2 - 15), width/2 - wall_thickness/2)
                       .rect(slot_width, wall_thickness + 2)
                       .cutBlind(-slot_depth)
                       
                       # Notch 3 (Back wall Right, +X) - assuming symmetry
                       .moveTo(length/2 - 15, -(width/2 - wall_thickness/2))
                       .rect(slot_width, wall_thickness + 2)
                       .cutBlind(-slot_depth)
                       
                       # Notch 4 (Back wall Left, -X) - assuming symmetry
                       .moveTo(-(length/2 - 15), -(width/2 - wall_thickness/2))
                       .rect(slot_width, wall_thickness + 2)
                       .cutBlind(-slot_depth)
                      )

# 4. Add fillets to the vertical outer corners
# The image shows rounded outer corners.
result = result_with_notches.edges("|Z").fillet(corner_radius)

# Note: The image also shows a "step" or ledge inside the walls, or perhaps the walls are just thick.
# The previous `rect` cut created simple vertical walls.
# Looking closer at the far corner, it seems to be a simple box cut.
# However, there is a horizontal line on the outside face. 
# This implies the bottom part might be a separate assembly or a decorative groove.
# Or, simpler explanation: It's a chamfer or a small reveal at the bottom.
# Let's add a small chamfer to the bottom edge to match that "line" look.
result = result.edges("<Z").chamfer(0.5)

# If the "line" on the side is a seam, it might be a split body, but for a single part model,
# a small groove or just the geometry as defined above is the most likely intended shape.
# Based on standard electronics enclosures, it's likely just a simple tray.

# Final assignment
result = result