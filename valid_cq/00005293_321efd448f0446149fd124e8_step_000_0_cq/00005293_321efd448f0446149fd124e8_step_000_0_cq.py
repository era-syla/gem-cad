import cadquery as cq

# --- Parametric Variables ---
# Overall dimensions
width = 200.0   # Total width of the shelving unit
height = 150.0  # Total height of the shelving unit
depth = 20.0    # Depth (thickness) of the unit

# Grid configuration
num_cols = 6    # Number of vertical columns
num_rows = 8    # Number of horizontal rows

# Material thickness
wall_thickness = 2.0  # Thickness of outer frame and internal dividers

# --- Derived Calculations ---
# Calculate the internal dimensions of each cell
# Total width = (num_cols * cell_width) + ((num_cols + 1) * wall_thickness)
# But looking at the image, the outer frame seems flush with the inner dividers.
# Let's assume uniform thickness for all vertical and horizontal members.

# Inner usable width
total_inner_width = width - (2 * wall_thickness)
# The space available for columns is split by (num_cols - 1) dividers
# However, it's easier to think of it as repeating units or just subtracting all material.

# Let's create the base block and cut out the cells.
cell_width = (width - (num_cols + 1) * wall_thickness) / num_cols
cell_height = (height - (num_rows + 1) * wall_thickness) / num_rows

# --- Geometry Construction ---

# 1. Create the main solid block (the outer bounds)
main_block = cq.Workplane("XY").box(width, height, depth)

# 2. Create the negative space (the "air" inside the shelves)
# We will create a single cell cutter and repeat it in a grid pattern.

# Create a single cell cutter
cell_cutter = (
    cq.Workplane("XY")
    .box(cell_width, cell_height, depth) # Cut all the way through initially
)

# 3. Create the grid of cutters
# We need to position the cutters correctly.
# Center-to-center spacing calculations:
col_spacing = cell_width + wall_thickness
row_spacing = cell_height + wall_thickness

# Using rarray to create the grid of cuts
# The rarray centers the grid at (0,0).
grid_cutters = (
    cq.Workplane("XY")
    .rarray(
        xSpacing=col_spacing, 
        ySpacing=row_spacing, 
        xCount=num_cols, 
        yCount=num_rows, 
        center=True
    )
    .box(cell_width, cell_height, depth) # The cutter for each position
)

# 4. Perform the cut
# We cut the grid from the main block.
# Note: The main_block has depth centered at Z=0. The cutters also have depth centered at Z=0.
# To make it a container with a back, we would offset the cut. 
# Looking at the image, it looks like a through-grid (open on both sides) or a very thin back.
# The shadow implies it might have a back panel. Let's assume a back panel for realism, 
# or just make it a through-hole structure if that's safer. 
# The prompt image looks like an open grid (see through). Let's stick to open grid for simplicity 
# and robustness, or leave a small back wall. 
# Let's make it an open grid as strictly interpreted from "grid structure". 
# But wait, usually these are shelves. Let's add a back panel option but set thickness to 0 
# (through cut) based on the pure "grid" look, or leave a thin back if desired.
# The image shows shadows inside the boxes, suggesting a back. Let's leave a 2mm back.

back_thickness = 2.0
cut_depth = depth - back_thickness

# Re-defining the cutter to respect the back panel
# We move the workplane to the front face and cut inwards
result = (
    cq.Workplane("XY")
    .box(width, height, depth) # Base solid
    .faces(">Z") # Select front face
    .workplane()
    .rarray(
        xSpacing=col_spacing, 
        ySpacing=row_spacing, 
        xCount=num_cols, 
        yCount=num_rows, 
        center=True
    )
    .rect(cell_width, cell_height) # Sketch the rectangles on the face
    .cutBlind(-cut_depth) # Cut into the solid, leaving the back wall
)

# Optional: Fillet the outer edges slightly for better rendering, though not strictly in the image
# result = result.edges().fillet(0.5) 

# Explicitly naming the result variable
result = result