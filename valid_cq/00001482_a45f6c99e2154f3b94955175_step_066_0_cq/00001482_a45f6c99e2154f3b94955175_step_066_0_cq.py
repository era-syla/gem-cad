import cadquery as cq

# Parametric dimensions
cylinder_od = 40.0
cylinder_id = 28.0
cylinder_length = 60.0
cylinder_offset_y = 10.0  # Vertical offset of the cylinder center

block_width = 30.0    # Width of the rectangular block section
block_height = 40.0   # Height of the main rectangular block section
block_length = 35.0   # Length sticking out from the cylinder area

slot_width = 2.0      # Width of the horizontal clamping slot
slot_depth = 20.0     # Depth of the clamping slot cut

bolt_hole_dia = 4.2   # Diameter for clamping bolts
top_bolt_hole_dia = 3.5

# Base mounting features
base_width = 40.0
base_length = 60.0 # Matches cylinder length roughly
base_height = 25.0
base_cutout_width = 20.0
base_cutout_height = 15.0

# Construction
# 1. Main Cylinder
# Create the main cylindrical housing
main_cyl = (
    cq.Workplane("XY")
    .circle(cylinder_od / 2.0)
    .extrude(cylinder_length)
    .translate((0, cylinder_offset_y, 0))
)

# 2. Rectangular Block (The clamp body)
# Attach a block to the side of the cylinder
block = (
    cq.Workplane("XY")
    .rect(block_length + cylinder_od/2, block_height, centered=False)
    .extrude(cylinder_length)
    .translate((-block_length - cylinder_od/2 + 5, -block_height/2 + cylinder_offset_y, 0))
)

# Combine Cylinder and Block
body = main_cyl.union(block)

# 3. Create the Base/Bottom structure
# There is a block underneath the main assembly, but it looks stepped
base_block = (
    cq.Workplane("XZ")
    .rect(base_width + 20, cylinder_length) # +20 to ensure intersection
    .extrude(base_height)
    .translate((-10, cylinder_length/2, -base_height/2 - block_height/2 + cylinder_offset_y + 10))
)
# Note: Position is approximate based on visual proportions. 
# The base sits under the main block/cylinder interface.

body = body.union(base_block)


# 4. Features and Cuts

# A. Cylinder Through Hole
body = (
    body.faces(">Z").workplane()
    .moveTo(0, cylinder_offset_y)
    .circle(cylinder_id / 2.0)
    .cutBlind(-cylinder_length)
)

# B. Horizontal Clamping Slot
# Cut a slot through the rectangular block to allow clamping
body = (
    body.faces("<X").workplane()
    .center(0, cylinder_offset_y) # Re-center Y relative to the block face
    .rect(block_length * 2, slot_width) # Extend width to ensure full cut
    .cutThruAll()
)

# C. Side Bolt Holes (for clamping)
# Two holes on the side face
body = (
    body.faces("<Z").workplane()  # Looking from side (actually Z is the length axis here based on extrude direction)
    .transformed(rotate=(0, 90, 0)) # Rotate to look at the side face
    .moveTo(cylinder_length * 0.25, cylinder_offset_y + 8)
    .circle(bolt_hole_dia / 2.0)
    .moveTo(cylinder_length * 0.25, cylinder_offset_y - 8)
    .circle(bolt_hole_dia / 2.0)
    .cutBlind(-block_width)
)

# D. Top Bolt Hole
body = (
    body.faces("<X").workplane() # Front face of the block
    .moveTo(-cylinder_length * 0.15, cylinder_offset_y + block_height/2 - 5)
    .circle(top_bolt_hole_dia / 2.0)
    .cutBlind(-15)
)

# E. Bottom Cutout (The L-shape cut at the bottom left in the image)
body = (
    body.faces("<Z").workplane() # Bottom face relative to extrusion
    .transformed(rotate=(0, 90, 0))
    .moveTo(0, -20) # Move down
    .rect(base_length, 20, centered=True) # Approximate large cut
    .cutBlind(20)
)
# Since orientation is getting tricky, let's use global coordinates for specific cuts
cut_box = (
    cq.Workplane("XY")
    .rect(30, 30)
    .extrude(30)
    .translate((-35, -25, -5))
)
body = body.cut(cut_box)

# F. The Rectangular hole beneath the cylinder (right side of image)
rect_hole = (
    cq.Workplane("YZ")
    .rect(12, 20)
    .extrude(20)
    .translate((0, cylinder_offset_y - cylinder_od/2 - 5, cylinder_length/2))
)
# Re-orient the rect hole to cut sideways through the web
rect_hole_cutter = (
    cq.Workplane("XY")
    .workplane(offset=cylinder_length/2) # Move to middle of length
    .transformed(rotate=(0, 0, 90))      # Rotate to face the side
    .moveTo(cylinder_offset_y - cylinder_od/2 - 4, 0)
    .rect(8, 18)
    .extrude(30) # Cut outwards
    .translate((0,0,-15)) # Center the cut
)
body = body.cut(rect_hole_cutter)

# G. Side recess (The curved pocket on the block side)
body = (
    body.faces(">Y").workplane(centerOption="CenterOfBoundBox")
    .moveTo(-15, 0)
    .circle(6)
    .cutBlind(-4)
)

# H. Fillets
# Apply fillets to the main vertical edges
try:
    body = body.edges("|Z").filter(lambda e: e.Center().x < 0 and e.Center().y > 0).fillet(2.0)
except:
    pass # Skip if selection fails based on specific topology

# Final cleanup rotation to match image orientation roughly
result = body.rotate((0,0,0), (1,0,0), -90).rotate((0,0,0), (0,0,1), -45)