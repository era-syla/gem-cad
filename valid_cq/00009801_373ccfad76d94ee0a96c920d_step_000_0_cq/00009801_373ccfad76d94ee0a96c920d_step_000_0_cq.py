import cadquery as cq

# Parameters
length = 100.0       # Total length of the part
width = 50.0         # Total width of the part
height_end = 30.0    # Height of the taller end walls
height_side = 10.0   # Height of the shorter side rails (lip)
thickness = 5.0      # Thickness of the walls and base
hole_diameter = 6.0  # Diameter of the holes in the base
hole_spacing = 30.0  # Distance between hole centers

# Create the main block
# We start with the overall bounding box and then cut away the material
base = cq.Workplane("XY").box(length, width, height_end)

# Cut the middle section to create the U-shape profile (the lower middle area)
# We need to cut away a volume from the top down to the base thickness
# The cut should leave the end walls and the side rails (if they exist, 
# but looking closely at the image, it seems to be a tray with high ends and low sides)

# Let's verify the geometry type:
# It looks like a rectangular base with two tall end plates and two shorter side walls.
# Actually, looking at the shadows and lines, it appears to be a solid block hollowed out.
# Or constructed from a base + walls.

# Construction Strategy:
# 1. Create the base plate.
# 2. Add the two tall end walls.
# 3. Add the two shorter side walls connecting the ends.
# 4. Cut the holes.

# Re-evaluating dimensions based on visual proportions:
# Length seems ~2x Width.
# Tall walls seem ~0.6x Width.
# Short walls seem ~0.2x Width.

# New construction approach using a sketch/profile extrusion might be cleaner, 
# but boolean subtraction from a block is very robust in CadQuery.

# Let's go with the subtraction method on a solid block.
# 1. Start with full block (L x W x H_end).
# 2. Cut the "inside" area.

# Inner dimensions
inner_length = length - (2 * thickness)
inner_width = width - (2 * thickness)

# Cutout logic:
# To leave the short side walls, the cut width must be slightly narrower than the full width,
# but wait, the image shows the short side walls are flush with the outside.
# So we cut the center, leaving a rim.
# The cut depth goes down to the base thickness.
# However, the end walls are TALLER than the side walls.

# Correct Strategy:
# 1. Create a base box (length x width x height_side).
# 2. Add the taller end walls on top of the ends.
# 3. Cut the pocket out of the base box to make the tray.
# OR
# 1. Extrude a U-profile for the length (base + side walls).
# 2. Add the end caps.
# 3. Cut holes.

# Let's try the additive approach, it's often more intuitive for this specific shape.

# Step 1: The Base Plate
result = cq.Workplane("XY").box(length, width, thickness)

# Step 2: The Tall End Walls
# We create one wall and mirror or create both.
end_wall = cq.Workplane("XY").workplane(offset=thickness/2).box(thickness, width, height_end - thickness)
# Move first wall to the front end
wall1 = end_wall.translate((length/2 - thickness/2, 0, (height_end - thickness)/2))
# Move second wall to the back end
wall2 = end_wall.translate((-length/2 + thickness/2, 0, (height_end - thickness)/2))

# Step 3: The Short Side Walls
# These run along the length between the end walls.
side_wall_length = length - (2 * thickness)
side_wall_height = height_side - thickness 
# Note: If side_wall_height <= 0, we just have a flat plate with ends. 
# Looking at the image, there IS a lip on the sides, creating a shallow tray.
side_wall = cq.Workplane("XY").workplane(offset=thickness/2).box(side_wall_length, thickness, side_wall_height)

# Move first side wall to the right
sw1 = side_wall.translate((0, width/2 - thickness/2, side_wall_height/2))
# Move second side wall to the left
sw2 = side_wall.translate((0, -width/2 + thickness/2, side_wall_height/2))

# Combine all parts
result = result.union(wall1).union(wall2).union(sw1).union(sw2)

# Step 4: Holes
# There are 3 holes along the center line.
# We can select the top face of the base and drill.
result = (
    result.faces("<Z")  # Select the bottom face
    .workplane()        # Create a workplane on it
    .pushPoints([(0, 0), (hole_spacing, 0), (-hole_spacing, 0)]) # Center, Left, Right
    .hole(hole_diameter)
)

# Refinement: Fillets?
# The image shows sharp edges, so no fillets required.