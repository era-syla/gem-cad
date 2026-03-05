import cadquery as cq

# Parameters for the Engine Block/Crankshaft Housing
num_cylinders = 4
total_length = 300.0
block_width = 120.0
block_height = 80.0

# Bearing Cap / Web parameters
web_thickness = 30.0  # Thickness of each bearing support wall
journal_diameter = 60.0 # Diameter of the crankshaft journal
journal_radius = journal_diameter / 2.0

# Base V-shape parameters
base_angle = 60 # Angle for the V shape at the bottom sides
bottom_thickness = 20.0 # Thickness of material below the journal

# Mounting Hole parameters
top_hole_diameter = 8.0
top_hole_spacing = 20.0 # Distance between the two holes on each flat top
top_hole_depth = 30.0

# Side hole parameters (oil gallery or cross bolts)
side_hole_diameter = 12.0
side_hole_height_offset = 15.0 # From the bottom curve center

# Derived Calculations
segment_pitch = total_length / num_cylinders 
# Wait, looking at the image, there are 5 "walls" for a 4-cylinder layout usually.
# Let's count the walls in the image: 1, 2, 3, 4, 5. So it's likely a 4-cylinder block frame (5 main bearings).
num_webs = 5
web_spacing = (total_length - web_thickness) / (num_webs - 1)

# Function to create a single bearing web profile
def create_web_profile(width, height, thickness, journal_r):
    # Base Sketch
    pts = [
        (width/2, height),      # Top Right
        (-width/2, height),     # Top Left
        (-width/2, height/2),   # Mid Left (start of angle)
        (-width/4, 0),          # Bottom Left
        (width/4, 0),           # Bottom Right
        (width/2, height/2),    # Mid Right (start of angle)
    ]
    
    # We will construct this by subtraction from a block to get the nice curves
    # Start with the main block shape
    
    # Let's define the outer hull
    # The shape is roughly a block with angled sides at the bottom
    
    # Create the basic trapezoidal/block shape
    shape = (
        cq.Workplane("XY")
        .moveTo(-width/2, 0)
        .lineTo(-width/2, height)
        .lineTo(width/2, height)
        .lineTo(width/2, 0)
        .lineTo(0, -height*0.3) # V-bottom point approximation
        .close()
        .extrude(thickness)
    )
    
    # Cut the main bearing semi-circle
    shape = shape.faces(">Y").workplane().center(0, height).cut(
        cq.Workplane("XZ").circle(journal_r).extrude(thickness*2)
    )

    # Cut the "U" shape between webs (this logic is better handled by making the whole block and cutting slots)
    return shape

# Strategy Revision: 
# Instead of making webs and joining them, make a solid block and cut away the material between webs.
# This ensures perfect alignment and continuous geometry.

# 1. Create the main stock material
stock = (
    cq.Workplane("XY")
    .moveTo(-block_width/2, 0)
    .lineTo(-block_width/2, block_height)
    .lineTo(block_width/2, block_height)
    .lineTo(block_width/2, 0)
    .lineTo(0, -block_height*0.25) # Bottom V point
    .close()
    .extrude(total_length)
)

# 2. Cut the main Crankshaft Bore (longitudinal)
# The image shows the bore going through the webs, but the space between webs is empty.
# However, the "U" shape cut removes the top part of the bore.
# Let's cut the bore first.
# The bore center is usually offset from the top face.
crank_center_y = block_height - journal_radius - 10.0 # 10mm material above bearing

stock = stock.faces(">Z").workplane().center(0, crank_center_y).cut(
    cq.Workplane("YZ").circle(journal_radius).extrude(total_length)
)

# 3. Create the Cutout shape to remove material between the webs
# We have 5 webs, so we need 4 cutouts.
cutout_width = segment_pitch - web_thickness 
# Actually, let's redefine based on the image: 5 distinct thick bearing caps.
# Let's assume total_length covers outside-to-outside.
# Spacing between centers of webs.
web_center_dist = total_length / (num_webs - 1)
cutout_length = web_center_dist - web_thickness

# We need a shape that represents the "void" between the bearing supports.
# It cuts from the top down, leaving the bottom spine (if there is one) or cutting through.
# Looking at the image, there is no bottom spine connecting them rigidly in the center; 
# they look like deep U-valleys. However, usually, they are connected at the bottom or sides.
# The image shows them connected by the lower "V" section (the oil pan rail area).

# Let's create a cutter that leaves the "V" base intact but removes the top block material.
cutter_profile_radius = block_width/2 * 0.8
cutter = (
    cq.Workplane("XY")
    .moveTo(-block_width, block_height + 10)
    .lineTo(block_width, block_height + 10)
    .lineTo(block_width, 0) # Depth of cut
    # Create a rounded bottom for the cut
    .threePointArc((0, -journal_radius * 1.5), (-block_width, 0))
    .close()
    .extrude(cutout_length)
)

# Perform the cuts
for i in range(num_webs - 1):
    # Calculate position
    # Start from one end
    offset = (web_thickness + cutout_length) * i + web_thickness
    
    # Translate the cutter
    # The stock was extruded in +Z from 0 to total_length
    current_cutter = cutter.translate((0, 0, offset))
    
    stock = stock.cut(current_cutter)

# 4. Refine the Crankshaft bore area
# The cut we just did might have messed up the perfect semi-circle saddle.
# We need to ensure the saddle is a perfect semi-circle on the remaining webs.
# Let's recut the main journal bore just to be clean across the webs.
# Position relative to the block geometry constructed in step 1.
# The profile in step 1 was drawn on XY. Extruded in Z.
# Y is "Height" in the 2D profile, but Z in world is usually height.
# Let's re-orient mental model:
# Step 1: XY plane profile. Y is vertical in profile. Extruded along Z.
# So "Top" of block is Y = block_height. "Bottom" is Y = -...
# "Front/Back" is Z. "Left/Right" is X.

# Let's add the bolt holes on the top faces of the webs.
# We need to select the top faces of the remaining webs.
# Top faces are roughly at Y = block_height.

# Helper to add holes to a specific web
def add_bolt_holes(shape, z_center):
    # Left holes
    shape = (
        shape.faces(">Y").workplane()
        .pushPoints([
            (-block_width/4 - 5, z_center + 5), 
            (-block_width/4 - 5, z_center - 5)
        ])
        .hole(top_hole_diameter, top_hole_depth)
    )
    # Right holes
    shape = (
        shape.faces(">Y").workplane()
        .pushPoints([
            (block_width/4 + 5, z_center + 5), 
            (block_width/4 + 5, z_center - 5)
        ])
        .hole(top_hole_diameter, top_hole_depth)
    )
    return shape

# Helper to add side cross-bolt holes
def add_side_holes(shape, z_center):
    # Hole going through the side boss
    # Axis is X.
    # Height is slightly below the journal center usually.
    h_y = crank_center_y - journal_radius - 5.0 
    
    shape = (
        shape.faces(">X").workplane(centerOption="CenterOfBoundBox")
        .moveTo(z_center, h_y) # Workplane coordinates are tricky on faces.
        # Let's stick to absolute coordinates for reliability.
        .transformed(offset=cq.Vector(0, 0, 0), rotate=cq.Vector(0, 90, 0)) # Rotate to align with X axis
    )
    
    # Simpler approach: Cylinder subtraction
    hole_cutter = (
        cq.Workplane("YZ")
        .circle(side_hole_diameter/2)
        .extrude(block_width + 20)
        .translate((-block_width/2 - 10, h_y, z_center))
    )
    return shape.cut(hole_cutter)

# Iterating to add details to each web
# We know the Z-centers of the webs.
# Web 1 center: web_thickness / 2
# Web 2 center: web_thickness + cutout_length + web_thickness/2
# ...

final_shape = stock

for i in range(num_webs):
    # Calculate Center Z of the current web
    center_z = (web_thickness/2) + i * (web_thickness + cutout_length)
    
    # Add Top Mounting Holes
    # We create a workplane on the top surface
    # Since the top surface is segmented, we can just cut blindly from a high plane
    
    # Create hole cutters for this web
    hole_positions = [
        (-block_width/2 + 15, center_z - 6),
        (-block_width/2 + 28, center_z + 6), # Staggered slightly looking at image? No, parallel.
        (-block_width/2 + 15 + 12, center_z - 6), # Two holes per side
    ]
    # Re-evaluating image: Looks like 2 holes per side per web. 
    # Aligned along the length.
    
    pts_left = [
        (-block_width/3, center_z - 5),
        (-block_width/3 - 12, center_z - 5) # Actually they look side-by-side relative to X
    ]
    
    # Let's align them properly based on the image
    # On the flat top faces: two holes on left, two holes on right.
    # They seem aligned along the X axis (transverse).
    
    top_z = block_height
    
    for x_side in [-1, 1]:
        x_base = x_side * (block_width/2 - 18)
        
        # Hole 1
        h1 = (
            cq.Workplane("XY")
            .circle(top_hole_diameter/2)
            .extrude(20)
            .translate((x_base, top_z, center_z - 4))
            .rotate((0,0,0), (1,0,0), -90) # Orient vertical down
        )
        
        # Hole 2
        h2 = (
            cq.Workplane("XY")
            .circle(top_hole_diameter/2)
            .extrude(20)
            .translate((x_base - x_side*12, top_z, center_z + 4)) # Slight offset
             .rotate((0,0,0), (1,0,0), -90)
        )
        
        # Simple vertical drilling
        final_shape = final_shape.cut(
            cq.Workplane("XY")
            .pushPoints([(x_base, center_z + 4), (x_base - x_side*15, center_z + 4)])
            .circle(top_hole_diameter/2)
            .extrude(block_height + 10) # Cut from 0 up?
            .translate((0, 0, 0)) # Reset
        )
        # The coordinate system is still: X=Left/Right, Y=Up, Z=Length
        # Holes come from +Y going down.
        
        # Correct Hole Logic
        hole_locs = [
            (x_base, center_z - 4),
            (x_base - x_side*12, center_z - 4) # Parallel to X axis
        ]
        
        final_shape = (
            final_shape
            .faces(">Y")
            .workplane()
            .pushPoints(hole_locs)
            .hole(top_hole_diameter, top_hole_depth)
        )

    # Add Side Holes (Oil/Cross-bolts)
    # Visible on the angled/side part of the web
    side_hole_y = block_height * 0.3
    
    # We just cut a cylinder through X
    final_shape = final_shape.cut(
        cq.Workplane("YZ")
        .circle(side_hole_diameter/2)
        .extrude(block_width*2) # Long enough to cut through
        .translate((-block_width, side_hole_y, center_z))
    )

# 5. Add the main Journal Saddles (Semi-circles)
# We already cut a hole earlier, but the "U" cut might have removed the top half.
# We ensure the saddle shape is correct by cutting the journal again.
final_shape = final_shape.cut(
    cq.Workplane("YZ")
    .circle(journal_radius)
    .extrude(total_length*2)
    .translate((-total_length/2, crank_center_y, 0)) # YZ plane is at X=0
    .rotate((0,0,0), (0,1,0), 90) # Rotate to align with Z
    # Wait, simple cylinder on YZ plane extruded in X? No.
    # Cylinder on XY extruded in Z? No.
    # Cylinder radius on XY plane?
)

# Simplest way to ensure bore is correct:
final_shape = final_shape.cut(
    cq.Workplane("XY") # Base plane
    .workplane(offset=0) # Z=0
    .transformed(rotate=(0, 90, 90)) # Orient for longitudinal cylinder
    .circle(journal_radius)
    .extrude(total_length)
    .translate((0, crank_center_y, 0)) # Move up to correct height
)

# 6. Fillets
# Apply fillets to the edges of the webs for the cast look
try:
    final_shape = final_shape.edges("|Y").fillet(2.0)
except:
    pass # Fillets can be fragile

# Re-orient for the standard ISO view (Y-up) if needed, 
# though CadQuery usually treats Z as up. 
# In this script:
# Z was used as the Longitudinal axis (Engine length).
# Y was used as Height.
# X was used as Width.
# To match the image where it sits "flat", this orientation is fine.

result = final_shape