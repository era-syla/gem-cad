import cadquery as cq

# --- Parametric Dimensions ---
# Overall dimensions of the block
block_length = 200.0
block_width = 100.0
block_height = 50.0

# Pattern parameters
num_cols = 10  # Number of holes along the length
num_rows = 5   # Number of holes along the height
wall_thickness = 2.0 # Thickness of the walls between holes and the outer edge

# --- Calculations ---
# Calculate the dimensions of individual rectangular holes based on the block size and wall thickness
# Total width available for holes = block_length - (wall_thickness * (num_cols + 1))
hole_length = (block_length - (wall_thickness * (num_cols + 1))) / num_cols

# Total height available for holes = block_height - (wall_thickness * (num_rows + 1))
hole_height = (block_height - (wall_thickness * (num_rows + 1))) / num_rows

# --- Geometry Construction ---

# 1. Create the main solid block
base_block = cq.Workplane("XY").box(block_length, block_width, block_height)

# 2. Define the face to cut (let's use the front face, defined by X and Z dimensions)
# We need to position a workplane on the front face to cut into it.
# The block is centered at origin, so the front face is at y = -block_width/2
# We work on the XZ plane.

# Center points calculation for the grid
# The grid starts relative to the center of the face.
# We create a list of (x, y) points for the centers of the rectangular holes on the 2D workplane.
points = []

# Calculate start positions (bottom-left most hole center relative to face center)
# The total span of hole centers is:
span_x = (num_cols - 1) * (hole_length + wall_thickness)
span_y = (num_rows - 1) * (hole_height + wall_thickness)

start_x = -span_x / 2
start_y = -span_y / 2

for r in range(num_rows):
    for c in range(num_cols):
        x = start_x + c * (hole_length + wall_thickness)
        y = start_y + r * (hole_height + wall_thickness)
        points.append((x, y))

# 3. Create the cut pattern
# We select the front face, push the points, sketch the rectangles, and cut blindly through.
# Since box is centered, the face is at Y = -block_width/2. We look at it from the front.
result = (
    base_block.faces("<Y")  # Select the front face
    .workplane()            # Create a workplane on that face
    .pushPoints(points)     # Push the grid of center points
    .rect(hole_length, hole_height) # Draw rectangles at all points
    .cutBlind(-block_width) # Cut through the entire width of the block
)

# Export or visualization would happen here, but only the 'result' variable is required.