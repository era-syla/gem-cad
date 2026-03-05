import cadquery as cq

# --- Parametric Dimensions ---
plate_width = 300.0   # Width of the square plate
plate_height = 300.0  # Height (depth) of the square plate
plate_thickness = 12.0 # Thickness of the plate

# Grid settings for the small holes
# Looking at the image, it looks like a roughly 10x10 grid, but some are missing or replaced
grid_rows = 10
grid_cols = 10
small_hole_diameter = 4.0
small_hole_spacing_x = plate_width / (grid_cols + 1)
small_hole_spacing_y = plate_height / (grid_rows + 1)

# Large holes (looks like counterbored or just larger clearance holes)
# There are 8 specific locations for larger holes visible in the image.
# They form a rotated rectangle or are somewhat centrally located.
large_hole_diameter = 10.0
large_hole_cbore_diameter = 16.0
large_hole_cbore_depth = 4.0

# Define coordinates for the larger holes relative to the center
# Based on visual approximation of the pattern:
# The pattern looks symmetric. Let's define a rough offset.
lh_offset_1 = 60.0
lh_offset_2 = 30.0

large_hole_locations = [
    # Inner rectangleish pattern
    (lh_offset_2, lh_offset_1), (lh_offset_2, -lh_offset_1),
    (-lh_offset_2, lh_offset_1), (-lh_offset_2, -lh_offset_1),
    # Outer/rotated pattern
    (lh_offset_1, lh_offset_2), (lh_offset_1, -lh_offset_2),
    (-lh_offset_1, lh_offset_2), (-lh_offset_1, -lh_offset_2),
]

# --- Modeling ---

# 1. Create the base plate
result = cq.Workplane("XY").box(plate_width, plate_height, plate_thickness)

# 2. Create the grid of small holes
# We generate a list of all grid points first
grid_points = []
for r in range(grid_rows):
    for c in range(grid_cols):
        # Calculate x and y based on centered grid
        x = (c - (grid_cols - 1) / 2) * small_hole_spacing_x
        y = (r - (grid_rows - 1) / 2) * small_hole_spacing_y
        
        # Check if this point is close to a large hole location. 
        # If so, skip it so we don't drill a small hole inside a large one.
        is_large_hole = False
        for lx, ly in large_hole_locations:
            if abs(x - lx) < 5.0 and abs(y - ly) < 5.0:
                is_large_hole = True
                break
        
        if not is_large_hole:
            grid_points.append((x, y))

# Cut the small holes
result = result.faces(">Z").workplane().pushPoints(grid_points).hole(small_hole_diameter)

# 3. Create the large holes (Counterbored)
# The image shows larger recesses, likely counterbores for socket head screws.
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(large_hole_locations)
    .cboreHole(large_hole_diameter, large_hole_cbore_diameter, large_hole_cbore_depth)
)

# Export or visualization would happen here in a real script, 
# but the prompt asks for the variable 'result'.