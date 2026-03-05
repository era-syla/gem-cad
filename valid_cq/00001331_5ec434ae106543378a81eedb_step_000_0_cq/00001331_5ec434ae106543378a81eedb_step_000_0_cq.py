import cadquery as cq

# -- Parameters --
# Block dimensions
block_length = 20.0
block_width = 10.0
block_height = 8.0

# Feature dimensions
circle_radius = 2.0
square_side = 3.0
feature_depth = 3.0  # Depth of the cuts
feature_offset = 5.0 # Distance from center for features

# Grid layout parameters
grid_spacing_x = 30.0
grid_spacing_y = 30.0
num_rows = 3
num_cols = 3

# -- Create a Single Unit --

# 1. Base block
unit = cq.Workplane("XY").box(block_length, block_width, block_height)

# 2. Add circular hole
# Located to the left of the center
unit = unit.faces(">Z").workplane().center(-feature_offset, 0).circle(circle_radius).cutBlind(-feature_depth)

# 3. Add square hole
# Located to the right of the center
# Note: CadQuery's rect() creates a rectangle centered at the current workplane center.
# We reset the center relative to the original face center.
unit = unit.faces(">Z").workplane().center(feature_offset, 0).rect(square_side, square_side).cutBlind(-feature_depth)

# -- Create the Grid Pattern --

# Initialize an empty assembly or list to hold the resulting solids
# We will use a loop to place copies of the unit
result_objects = []

# Calculate starting offsets to center the grid (optional, but good practice)
start_x = -((num_cols - 1) * grid_spacing_x) / 2
start_y = -((num_rows - 1) * grid_spacing_y) / 2

for r in range(num_rows):
    for c in range(num_cols):
        # Calculate position
        pos_x = start_x + c * grid_spacing_x
        pos_y = start_y + r * grid_spacing_y
        
        # Translate the unit to the new position
        new_unit = unit.translate((pos_x, pos_y, 0))
        result_objects.append(new_unit)

# Combine all objects into a single compound object for the final result
# Alternatively, we could iterate and union them, but creating a compound is often cleaner for "assemblies" of loose parts.
if result_objects:
    result = result_objects[0]
    for obj in result_objects[1:]:
        result = result.union(obj)
else:
    result = unit

# -- Export/Display --
# The 'result' variable is now available for CQ-editor or export
# show_object(result)