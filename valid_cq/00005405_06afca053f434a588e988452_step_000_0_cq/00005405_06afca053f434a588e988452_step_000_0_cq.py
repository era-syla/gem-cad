import cadquery as cq

# --- Parameter Definitions ---
# Overall dimensions
length = 150.0       # Total length of the rib structure
height_large = 50.0  # Height at the large end
height_small = 20.0  # Height at the small end
width = 20.0         # Width (thickness) of the rib structure
wall_thickness = 2.0 # Thickness of the outer walls and internal ribs

# Boss details
boss_dia = 6.0       # Outer diameter of the screw bosses/corner radii
hole_dia = 3.0       # Inner diameter of the mounting holes

# Internal structure
num_ribs = 4         # Number of internal vertical stiffeners

# --- Geometry Construction ---

# 1. Create the base profile sketch (Trapezoidal shape from top view perspective)
# Actually, looking at the image, it's a side profile extrusion.
# Let's model it as an extrusion from the side profile, then shell or pocket it.

# Define the side profile (trapezoid)
pts = [
    (0, 0),
    (length, 0),
    (length, height_small),
    (0, height_large)
]

# Create the main solid block first
base_solid = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(width)
)

# 2. Add the cylindrical bosses/rounded ends
# The image shows rounded columns at the three corners (two at large end, one at small end).
# Actually, looking closely, it seems like a single structural rib with bosses at the corners.
# Let's refine: It looks like two parallel walls with ribs in between.
# Let's try a different approach: Build the footprint and extrude up? No, the top is slanted.
# Let's stick to the side profile extrusion, but refine the ends.

# Let's create the outer shape with the bosses integrated.
# The "bosses" run the full height.

# Re-strategy:
# 1. Create a sketch of the top-down view? No.
# 2. Create the side profile. Extrude it.
# 3. Add cylinders at the corners for the bosses.
# 4. Hollow out the inside to create the walls.
# 5. Add the internal ribs.

# Let's construct the main body with rounded ends properly.
# We will create a sketch on the XZ plane (side view) and extrude Y (width).
# Wait, standard orientation usually has Z up. Let's build on XZ plane and extrude Y.

# Side profile points
x_start = 0
x_end = length
y_bottom = 0
y_top_start = height_large
y_top_end = height_small

# Create the main body
main_body = (
    cq.Workplane("XY")
    .moveTo(x_start, y_bottom)
    .lineTo(x_end, y_bottom)
    .lineTo(x_end, y_top_end)
    .lineTo(x_start, y_top_start)
    .close()
    .extrude(width)
)

# Add cylinders at the vertical edges (the "bosses")
# Boss 1: Large end, corner 1
boss_large = (
    cq.Workplane("XY")
    .circle(boss_dia / 2)
    .extrude(height_large)
)

# Boss 2: Small end
boss_small = (
    cq.Workplane("XY")
    .center(length, 0)
    .circle(boss_dia / 2)
    .extrude(height_small)
)

# Combine bosses with main body
# We need to center the main body extrusion relative to the bosses if we want the bosses centered on the wall
# The image shows the bosses are circular protrusions at the ends of the walls.
# Let's center the main body extrusion on Z=0 (which is our width axis in this specific operation context, effectively)
# Actually, let's just move the main body to align.
main_body = main_body.translate((0, 0, -width/2))

# We need two bosses at the large end? The image shows two bosses at the large end (top and bottom of the trapezoid base if viewed from side), 
# but wait, looking at the image orientation:
# It's a long triangular-ish truss. 
# There is a vertical post at the tall end.
# There is a vertical post at the short end.
# There are two parallel thin walls connecting them.
# There are internal ribs.
# AND there are holes going vertically through the posts.

# Revised Strategy:
# 1. Create the solid envelope (Trapezoidal prism + Cylinders at ends).
# 2. Shell it (hollow it out from the top).
# 3. Add internal ribs.
# 4. Cut the through holes.

# 1. Solid Envelope
# Left Cylinder (Tall)
c_left = cq.Workplane("XY").circle(boss_dia/2).extrude(height_large)

# Right Cylinder (Short)
c_right = cq.Workplane("XY").center(length, 0).circle(boss_dia/2).extrude(height_small)

# Connecting Wedge
# We need tangent lines between the two circles. For simplicity, just a rectangular connection reduced by width.
wedge = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(length, 0)
    .lineTo(length, height_small)
    .lineTo(0, height_large)
    .close()
    .extrude(boss_dia) # Initial thickness matches boss diameter
    .translate((0, 0, -boss_dia/2)) # Center it on Z
    # Now rotate it so "width" is the thickness, and height is Z
    .rotate((0,0,0), (1,0,0), 90)
    .translate((0, width/2, 0)) # Re-center on Y
)
# Re-orienting to make Z up, X length, Y width.
# The wedge needs to be tangent to the cylinders. 
# Let's just fuse the cylinders and a rectangular block, then cut the excess if needed.
# Simple approximation: A hull of the two cylinders? No, height differs.

# Let's build the outer shape using a Loft?
# Bottom profile: Two circles connected by tangent lines.
# Top profile: Two circles connected by tangent lines (but at different Z heights).

# Let's stick to simple boolean construction.
# Main block
points = [(0, 0), (length, 0), (length, height_small), (0, height_large)]
main_block = (
    cq.Workplane("XZ") # Draw on side
    .polyline(points)
    .close()
    .extrude(width) # Extrude width
    .translate((0, -width/2, 0)) # Center on Y
)

# Add Cylinders at ends
cyl_left = (
    cq.Workplane("XY")
    .circle(boss_dia/2)
    .extrude(height_large)
)
cyl_right = (
    cq.Workplane("XY")
    .center(length, 0)
    .circle(boss_dia/2)
    .extrude(height_small)
)

# Fuse them
solid = main_block.union(cyl_left).union(cyl_right)

# 2. Hollow out (Shelling)
# We want to remove the "top" face (which is actually the slanted face) and the bottom face?
# The image shows an open structure like a ladder frame or truss. 
# It has side walls, a bottom floor? No, looking closely, it creates a "U" channel or "H" channel?
# It looks like an open pocket from the top (the slanted side).
# But the bottom is flat. 
# Let's assume it's a "U" channel profile extruded along the length, but the height varies.

# Create the "cutout" shape to hollow the inside
# We need to subtract a smaller version of the main block.
inner_width = width - 2*wall_thickness
inner_length = length - boss_dia # Roughly inside the bosses
inner_height_large = height_large
inner_height_small = height_small

# To get the uniform wall thickness on the slanted part, it's tricky with simple scaling.
# We will cut a pocket from the top (Y-positive direction relative to the slanted face?)
# Let's just cut a block out of the middle.

cutout_block = (
    cq.Workplane("XZ")
    .moveTo(wall_thickness, wall_thickness) # Start inside wall
    .lineTo(length - wall_thickness, wall_thickness)
    .lineTo(length - wall_thickness, height_small - wall_thickness) # Keep top wall thickness? 
    # The image shows open top. So we go higher than the part to cut through.
    .lineTo(length - wall_thickness, height_small + 10) 
    .lineTo(wall_thickness, height_large + 10)
    .close()
    .extrude(inner_width)
    .translate((0, -inner_width/2, 0))
)

hollowed = solid.cut(cutout_block)

# 3. Internal Ribs
# We need to add ribs back into the hollow space.
# We can just union thin blocks spaced along the length.

rib_spacing = (length - 2*wall_thickness) / (num_ribs + 1)
ribs = cq.Workplane("XZ")

for i in range(1, num_ribs + 1):
    x_pos = wall_thickness + i * rib_spacing
    # Calculate height at this x position based on the slope
    # Slope equation: y = mx + c
    slope = (height_small - height_large) / length
    y_limit = height_large + slope * x_pos
    
    # Create rib geometry
    # It needs to fit inside the inner width
    rib_geo = (
        cq.Workplane("XY")
        .center(x_pos, 0) # Position in X
        .rect(wall_thickness, inner_width) # Footprint
        .extrude(y_limit - 2.0) # Extrude up to just below the top edge for aesthetics, or full height
    )
    # Actually, let's just make a large block and intersect it with the main solid to trim perfectly.
    
    rib_cutter = (
        cq.Workplane("XZ")
        .moveTo(x_pos - wall_thickness/2, 0)
        .lineTo(x_pos + wall_thickness/2, 0)
        .lineTo(x_pos + wall_thickness/2, height_large) # Overshoot height
        .lineTo(x_pos - wall_thickness/2, height_large)
        .close()
        .extrude(inner_width)
        .translate((0, -inner_width/2, 0))
    )
    
    # We unite this rib with the hollowed body. 
    # To ensure it doesn't stick out top, we intersect it with the original solid geometry first?
    # Or just rely on the fact we are adding it inside the pocket.
    
    # Better way: Create the ribs solid, intersect with the original 'solid' (before hollow), then union with 'hollowed'.
    
    # Let's make the ribs part of the original cutout logic (masking the cut).
    # That's harder.
    
    # Let's just create a rib block and intersect it with the original outer shape to get the correct top slope.
    rib_raw = (
        cq.Workplane("XZ")
        .moveTo(x_pos - wall_thickness/2, wall_thickness) # Start above bottom floor
        .lineTo(x_pos + wall_thickness/2, wall_thickness)
        .lineTo(x_pos + wall_thickness/2, height_large + 10)
        .lineTo(x_pos - wall_thickness/2, height_large + 10)
        .close()
        .extrude(inner_width)
        .translate((0, -inner_width/2, 0))
    )
    
    # Trim rib to the outer envelope
    trimmed_rib = rib_raw.intersect(solid)
    hollowed = hollowed.union(trimmed_rib)

# 4. Holes in Bosses
# Drill through the centers of the cylinders
final_part = (
    hollowed
    .faces("<Z") # Select bottom face
    .workplane()
    .moveTo(0, 0) # Center of left boss (relative to global origin which is center of left boss)
    .circle(hole_dia/2)
    .cutThruAll()
    .moveTo(length, 0) # Center of right boss
    .circle(hole_dia/2)
    .cutThruAll()
)

# 5. Fillets
# The image shows fillets on the internal pockets.
# Getting all vertical edges inside the pocket.
# This can be fragile in CAD kernels, so we select carefully.
# We want edges that are parallel to Z, and are "concave" relative to the empty space?
# Or we can fillet the rib intersections.
try:
    final_part = final_part.faces("|Y").edges(cq.selectors.TypeSelector("LINE")).fillet(1.0)
except:
    # Fallback if complex selection fails, just return un-filleted
    pass

result = final_part