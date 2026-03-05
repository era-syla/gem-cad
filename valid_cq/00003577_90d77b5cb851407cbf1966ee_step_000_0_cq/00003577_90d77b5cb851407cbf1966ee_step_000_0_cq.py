import cadquery as cq

# --- Parameter Definitions ---
plate_width = 100.0   # Width of the square plate
plate_height = 100.0  # Height (depth) of the square plate
plate_thickness = 10.0 # Thickness of the plate

grid_pitch = 2.5      # Distance between the centers of the grid cells
wall_thickness = 0.4  # Thickness of the walls between grid cells
cut_depth = 1.0       # Depth of the grid indentations

# Calculate grid cell size based on pitch and wall thickness
# cell_size + wall_thickness = grid_pitch
cell_size = grid_pitch - wall_thickness

# Calculate how many cells fit in X and Y
# We want to center the grid, so we calculate the count and then position
num_x = int((plate_width - wall_thickness) / grid_pitch)
num_y = int((plate_height - wall_thickness) / grid_pitch)

# --- Geometry Construction ---

# 1. Create the base plate
base = cq.Workplane("XY").box(plate_width, plate_height, plate_thickness)

# 2. Create the grid pattern
# We create a single rect for the cut, then apply rarray (rectangular array)
# to replicate it across the surface.

# We select the top face
grid_cuts = (
    base.faces(">Z")
    .workplane()
    # Use rarray to create the grid points. 
    # x_spacing, y_spacing, x_count, y_count, center=True
    .rarray(grid_pitch, grid_pitch, num_x, num_y, True)
    .rect(cell_size, cell_size)
    .cutBlind(-cut_depth)
)

result = grid_cuts