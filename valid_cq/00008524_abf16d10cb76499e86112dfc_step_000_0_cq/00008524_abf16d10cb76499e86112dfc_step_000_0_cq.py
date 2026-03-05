import cadquery as cq

# --- Parametric Dimensions ---
# Based on the grid lines in the image, the object appears to be a 
# rectangular plate with a 4x8 grid structure.
# We will define the size of a single "grid unit" to drive the geometry.

grid_size = 20.0       # Size of one square in the grid
rows = 4               # Number of rows (depth)
cols = 8               # Number of columns (width)
thickness = 2.0        # Thickness of the plate

# Derived dimensions
total_width = cols * grid_size
total_depth = rows * grid_size

# Notch dimensions
# The notch appears to be 1 grid unit wide and 1 grid unit deep, 
# located slightly off-center or centered on the grid lines. 
# Looking at the image:
# The front edge has 8 units. 
# From left to right: 3 full units, then a cut, then 4 full units? 
# Or maybe it's 2 units wide?
# Let's look closer. The cut seems to correspond to one of the grid squares.
# It looks like the cut is 1 unit deep and 1 unit wide.
# Its position: There are 4 columns to the left of the cut area, 
# and 3 columns to the right (total 8 columns is incorrect, let's recount).
# Left side: 4 units. Right side: 3 units. Total: 7 units + 1 cut? Or 8 units total?
# Let's assume an 8x4 grid for symmetry, but the cut is offset.
# Visual count:
# Left block: 4 units wide.
# Cut: 1 unit wide.
# Right block: 3 units wide.
# Total width = 4 + 1 + 3 = 8 units.
# Cut depth = 1 unit.

notch_width = grid_size
notch_depth = grid_size
notch_x_offset = (grid_size / 2) # Offset from center. 
# Center of plate is at x=0. 
# Total width is 8*grid. Left edge is -4*grid. Right edge is +4*grid.
# Cut starts at index 4 (0-based) or is the 5th block.
# Center of 5th block is at: -4*grid (start) + 4*grid (4 blocks) + 0.5*grid = 0.5*grid.
# Let's position the cut precisely based on this grid logic.

# --- Modeling ---

# 1. Create the base plate centered on XY plane
base_plate = cq.Workplane("XY").box(total_width, total_depth, thickness)

# 2. Create the notch geometry
# We will cut a rectangular chunk out of the front edge.
# The front edge in CadQuery default orientation (Y-up) is -Y direction? 
# Standard box is centered. Y goes from -total_depth/2 to +total_depth/2.
# Let's assume "front" in the image corresponds to -Y edge.

# Calculate center position of the cut
# The cut is the 5th unit from the left (index 4).
# Left edge X coord: -total_width / 2
# Center of 1st unit: -total_width/2 + grid_size/2
# Center of 5th unit: -total_width/2 + grid_size/2 + 4 * grid_size
cut_center_x = -total_width/2 + 4.5 * grid_size
cut_center_y = -total_depth/2 + notch_depth/2

# Create the cut
# We align the cutting tool relative to the center of the notch location
result = (
    base_plate
    .faces("<Z") # Select bottom face to work relative to it (or just rely on absolute coords)
    .workplane(centerOption="CenterOfMass")
    .moveTo(cut_center_x, cut_center_y)
    .rect(notch_width, notch_depth)
    .cutThruAll() 
)

# Optional: To make the grid lines visible like in the image (as physical geometry),
# we would typically add small grooves. However, usually these are just visual aids
# or separate tiles. Assuming the prompt wants a single solid representing the
# shape, the code above is sufficient. 
# If the grid lines represent physical grooves, we can add them.
# The prompt image looks like a single solid with a tessellation pattern, 
# but often these imply tiles. I will stick to the main solid geometry 
# as standard CAD practices usually don't model texture lines unless requested.

# Final Result
result = result
