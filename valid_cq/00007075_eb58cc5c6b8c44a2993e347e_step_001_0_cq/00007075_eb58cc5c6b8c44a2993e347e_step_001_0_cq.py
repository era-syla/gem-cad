import cadquery as cq

# -- Parameters --
# Overall Dimensions
block_width = 80.0
block_height = 80.0
block_depth = 40.0

# Top Plate Features
large_hole_diam = 20.0
small_hole_diam = 6.0
large_hole_spacing_x = 40.0  # Distance between centers of large holes
small_hole_spacing_x = 40.0
small_hole_spacing_y = 25.0

# Fin Parameters
fin_thickness = 4.0   # Thickness of the solid material
gap_thickness = 4.0   # Thickness of the empty space
top_plate_thickness = 10.0 # Solid block at the top
back_wall_thickness = 10.0 # Solid block at the back

# -- Construction --

# 1. Create the main solid block
base = cq.Workplane("XY").box(block_width, block_height, block_depth)

# 2. Create the fins by cutting slots
# We need to determine how many fins fit.
# The cuts start from the bottom and go up until the top plate.
cut_depth = block_depth - back_wall_thickness
available_height = block_height - top_plate_thickness
num_slots = int(available_height / (fin_thickness + gap_thickness))

# We'll create a profile for the cuts on the side face (YZ plane) or front face (XZ plane)
# Let's cut from the front face (XZ) going inwards (Y direction in this orientation, 
# but based on box creation "XY", height is Y, depth is Z. Let's re-orient mentally).
#
# Re-orienting for clarity:
# Let's assume the top face with holes is "XY".
# Width (X) = 80
# Depth (Y) = 40
# Height (Z) = 80
# The fins are horizontal cuts into the front face (XZ plane effectively, if viewed from front).

# Let's start fresh with a more logical orientation for CadQuery 
# Default Workplane("XY") is the ground. Let's make the top face the workplane for holes later.
# So the block sits on the ground.
# X = Width = 80
# Y = Depth = 40
# Z = Height = 80

result = cq.Workplane("XY").box(block_width, block_depth, block_height)

# 3. Cut the Fins
# The fins are slots cut into the front face (which is at Y = -block_depth/2).
# We want to cut rectangles out of the block.
# We skip the top section (top_plate_thickness).
# We skip the back section (back_wall_thickness).

slot_depth = block_depth - back_wall_thickness
start_z = -block_height/2 + gap_thickness/2 # Starting near bottom

for i in range(num_slots):
    # Calculate Z height for this specific slot center
    # Fins and gaps alternate. 
    # Let's say bottom is solid. Then a gap. Then solid.
    # Z position needs to be calculated relative to the center of the block.
    
    # Let's model this by selecting the front face and making rectangular cuts
    # The front face is at Y = -block_depth/2
    
    # Height of the cut center relative to the bottom of the block (0 to 80)
    h_from_bottom = (i * (fin_thickness + gap_thickness)) + fin_thickness + (gap_thickness/2)
    
    # Convert to coordinate system where Z=0 is center of block
    z_coord = h_from_bottom - (block_height/2)
    
    # Perform the cut
    # We select the front face, create a workplane, move to correct height
    result = (result.faces("<Y").workplane(centerOption="CenterOfMass")
              .center(0, z_coord)
              .rect(block_width, gap_thickness)
              .cutBlind(-slot_depth) # Cut inwards (negative direction relative to face normal)
             )

# 4. Create Top Holes
# Select the top face (Z > 0)
top_face = result.faces(">Z").workplane()

# Large Holes
# Assuming they are centered on the Y-axis of the top face, spaced in X
result = (top_face
          .pushPoints([(-large_hole_spacing_x/2, 0), (large_hole_spacing_x/2, 0)])
          .hole(large_hole_diam)
         )

# Small Holes
# These look like 4 holes in a rectangular pattern around the center
# Or perhaps 2 holes centered between the large ones? 
# Looking at the image: 
# There are two large holes.
# There are four small holes arranged in a rectangle.
# The small holes seem to be aligned or slightly offset from the large ones.
# Let's assume a symmetric rectangular pattern.

small_hole_locs = [
    (-small_hole_spacing_x/2, -small_hole_spacing_y/2),
    (small_hole_spacing_x/2, -small_hole_spacing_y/2),
    (-small_hole_spacing_x/2, small_hole_spacing_y/2),
    (small_hole_spacing_x/2, small_hole_spacing_y/2)
]

# We need to re-select the top face because the previous operation modified the object
# and the fluent API chain might have changed context.
result = (result.faces(">Z").workplane()
          .pushPoints(small_hole_locs)
          .hole(small_hole_diam)
         )