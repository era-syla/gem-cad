import cadquery as cq

# --- Parametric Dimensions ---
# Overall Dimensions
part_length = 120.0  # Total length of the part
part_width = 50.0    # Total width of the top plate
plate_thickness = 5.0 # Thickness of the main flat plate

# Vertical Flange Dimensions
flange_height = 25.0  # Max height of the side flange (from bottom to top surface)
flange_width = 10.0   # Width of the bottom ledge of the flange

# Cutout Dimensions
circular_hole_dia = 20.0
square_hole_side = 25.0

# Small Mounting Holes
small_hole_dia = 3.5

# --- Geometry Construction ---

# 1. Create the main top plate
# We'll center it mostly, then cut and add features.
top_plate = (
    cq.Workplane("XY")
    .box(part_length, part_width, plate_thickness)
)

# 2. Create the side wedge/flange structure
# This is the complex part. It looks like a vertical wall that tapers.
# Let's sketch the profile on the side face (XZ plane equivalent relative to the box).
# We need to position it on the side of the existing plate.

# Calculate the start point relative to the box center
# Box center is (0,0,0). Y extents are +/- part_width/2.
side_face_y = -part_width / 2.0

# Define the wedge profile coordinates
# (0,0) is bottom left of the sketch
p0 = (0, 0)
p1 = (part_length, 0)
p2 = (part_length, flange_height - plate_thickness) # Matches top surface height
p3 = (0, 0) # Back to start, forming a triangle

wedge_profile = (
    cq.Workplane("XZ")
    .center(0, -part_width/2 + flange_width/2) # Move to the side
    .workplane(offset=0) # Working on XZ plane at Y location
    .moveTo(-part_length/2, -plate_thickness/2 - (flange_height - plate_thickness))
    .lineTo(part_length/2, -plate_thickness/2)
    .lineTo(part_length/2, -plate_thickness/2 - (flange_height - plate_thickness))
    .close()
    .extrude(flange_width)
)

# Combine plate and wedge (Note: this is an approximation, let's refine the shape)
# Looking closely at the image, it's an 'L' bracket shape where the vertical leg is triangular.
# Actually, it looks like a solid block with a large triangular cut removed, or an extrusion of an L-shape that is then cut.
# Let's try a different approach: Build the base L-shape profile and extrude, then cut the taper.

# New Approach:
# Base Profile: L-shape
l_profile = (
    cq.Workplane("YZ")
    .moveTo(0,0)
    .lineTo(part_width, 0)
    .lineTo(part_width, plate_thickness)
    .lineTo(flange_width, plate_thickness) # Top of flange ledge
    .lineTo(flange_width, flange_height)   # Up the vertical wall? No, down.
    # Let's restart coordinate system logic.
    # Let origin be top-left corner on the surface.
)

# Let's stick to simple composition.
# Part A: The Top Plate
part_a = cq.Workplane("XY").box(part_length, part_width, plate_thickness)

# Part B: The Side Triangular Wall/Ledge
# We need a shape that starts at one end with height = flange_height and tapers to just the plate thickness at the other end.
# Actually, the image shows a consistent "L" shape where the vertical leg gets shorter.
# Or rather, a side block that is cut diagonally.

# Let's make a block on the side.
side_block = (
    cq.Workplane("XY")
    .workplane(offset=-flange_height/2 + plate_thickness/2) # Center Z
    .box(part_length, flange_width, flange_height)
    .translate((0, -part_width/2 + flange_width/2, -plate_thickness/2)) # Align with side and bottom of plate
)

# Move side_block down so its top is flush with plate top?
# The image shows the top surface is continuous.
# Let's align top surfaces.
side_block = (
    cq.Workplane("XY")
    .box(part_length, flange_width, flange_height)
    .translate((0, -part_width/2 + flange_width/2, -flange_height/2 + plate_thickness/2))
)

# Now union them
base_shape = part_a.union(side_block)

# Now apply the large diagonal cut (chamfer/cut) to the bottom of the side block
# We want to slice off the bottom triangle.
# Point A: Bottom corner at the "thin" end of the wedge
# Point B: Top corner (under the plate) at the "thick" end
# Point C: Bottom corner at the "thick" end (to define the material to keep or remove)

cut_wedge = (
    cq.Workplane("XZ")
    .moveTo(-part_length/2, -plate_thickness/2) # Start under the plate at left end
    .lineTo(part_length/2, -flange_height + plate_thickness/2) # Bottom right corner
    .lineTo(-part_length/2, -flange_height + plate_thickness/2) # Bottom left corner
    .close()
    .extrude(part_width + 10) # Extrude through the whole width to be safe
    .translate((0, -part_width/2 - 5, 0)) # Position in Y
)

# The cut above is tricky to align perfectly without robust references. 
# Let's model the geometry directly as a loft or ruled surface if needed, but simple cuts are better.

# Let's Try Approach 3: Constructive Solid Geometry from primitives.
# 1. Top Plate
plate = cq.Workplane("XY").box(part_length, part_width, plate_thickness)

# 2. Side Support (The L-leg)
# It's a block on the side, width=flange_width, length=part_length.
# Height varies.
# Let's make a full height block and cut it.
side_wall_full = (
    cq.Workplane("XY")
    .box(part_length, flange_width, flange_height)
    .translate((0, -part_width/2 + flange_width/2, -flange_height/2 + plate_thickness/2))
)

# Combine
combined = plate.union(side_wall_full)

# Cut the slope
# We want to keep the full height at x = +part_length/2 (right side in image?)
# And taper to zero extra height at x = -part_length/2.
# Looking at image:
# Left side: Just the plate.
# Right side: Full L-bracket height.
# Slope goes from bottom-right corner up to bottom of plate at left.

cutter = (
    cq.Workplane("XZ")
    .moveTo(-part_length/2, -plate_thickness/2) # Under plate, left
    .lineTo(part_length/2, -plate_thickness/2)  # Under plate, right
    .lineTo(-part_length/2, -flange_height)       # Deep point, left (Wait, slope is opposite)
    
    # Correct Slope logic based on image:
    # The part is thickest at one end (let's say Right) and thinnest at the Left.
    # The top surface is flat.
    # We need to remove a triangle from the bottom.
    
    .moveTo(-part_length/2 * 1.1, -plate_thickness/2) # Start Left, just under plate
    .lineTo(part_length/2 * 1.1, -plate_thickness/2)  # Go Right
    .lineTo(-part_length/2 * 1.1, -flange_height * 1.5) # Go Deep Left
    .close()
    .extrude(part_width * 2) # Make it wide
    .translate((0, -part_width/2, 0))
)

# Actually, simply cutting the side wall is easier.
# Let's define the side wall shape explicitly using a polyline and extrude.
# Side profile (XZ plane):
# (left_x, top_z), (right_x, top_z), (right_x, bottom_z), (left_x, top_z_minus_plate) -> NO
# The diagonal connects (Left_X, Bottom_of_Plate_Z) to (Right_X, Bottom_of_Flange_Z)
side_wall_profile = (
    cq.Workplane("XZ")
    .moveTo(-part_length/2, -plate_thickness/2)
    .lineTo(part_length/2, -plate_thickness/2)
    .lineTo(part_length/2, -flange_height + plate_thickness/2)
    .close() # Creates the triangle under the plate
    .extrude(flange_width)
    .translate((0, -part_width/2 + flange_width/2, 0))
)

base_solid = plate.union(side_wall_profile)


# --- Features (Holes and Cutouts) ---

# 1. Circular Hole (Large)
# Located towards the left
res_with_circle = (
    base_solid.faces(">Z")
    .workplane()
    .center(-part_length/4, 0)
    .circle(circular_hole_dia/2)
    .cutBlind(-plate_thickness*2) # Cut through
)

# 2. Square Cutout
# Located in the middle/right
res_with_square = (
    res_with_circle.faces(">Z")
    .workplane()
    .center(part_length/8, 0)
    .rect(square_hole_side, square_hole_side)
    .cutBlind(-plate_thickness*2)
)

# 3. Mounting holes (small)
# Four holes on the plate corners (roughly)
# One hole on the flange ledge at the deep end
# Two holes flanking the square cutout?
# Let's interpret the image dots.
# - Two near the right edge corners
# - One near the square cutout (bottom right relative to square)
# - One near the square cutout (top left relative to square)
# - One on the flange at the thick end.

# Let's define locations
holes_x_offset = part_length/2 - 10
holes_y_offset = part_width/2 - 8

# Right side corner holes
res_with_corner_holes = (
    res_with_square.faces(">Z")
    .workplane()
    .pushPoints([(holes_x_offset, holes_y_offset), (holes_x_offset, -holes_y_offset)])
    .circle(small_hole_dia/2)
    .cutBlind(-plate_thickness*2)
)

# Middle holes (around square)
# Visually estimated positions
mid_hole_1 = (0, -part_width/4) # Below square/circle gap
mid_hole_2 = (part_length/4, part_width/4 - 2) # Top right of square

res_with_mid_holes = (
    res_with_corner_holes.faces(">Z")
    .workplane()
    .pushPoints([(-5, -15), (35, 10)]) # Adjusted relative to center
    .circle(small_hole_dia/2)
    .cutBlind(-plate_thickness*2)
)

# Flange hole
# Located on the bottom ledge of the side wall (at the thick end)
# We need to select the face of the ledge.
# Since the ledge is a simple flat face created by the extrusion of the triangle.
# Center of the hole is roughly at x=part_length/2 - 10, y on the flange.

# Since the side wall was extruded centered on Y = -part_width/2 + flange_width/2
# We can just cut from the top, ensuring we go deep enough.
flange_hole_x = part_length/2 - 15
flange_hole_y = -part_width/2 + flange_width/2

final_model = (
    res_with_mid_holes.faces(">Z")
    .workplane()
    .moveTo(flange_hole_x, flange_hole_y)
    .circle(small_hole_dia/2)
    .cutBlind(-flange_height*2)
)

# There is a small notch in the large circular hole in the image (keyway).
# Let's add that.
final_model = (
    final_model.faces(">Z")
    .workplane()
    .center(-part_length/4, 0) # Center of circle
    .moveTo(circular_hole_dia/2, 0)
    .rect(3, 3) # Small square for keyway
    .cutBlind(-plate_thickness*2)
)

result = final_model