import cadquery as cq

# Parameters for the plate dimensions
width = 200.0
height = 260.0
thickness = 15.0

# Parameters for the hole configuration
hole_diameter = 6.0
margin_x = 25.0       # Distance from vertical edges
margin_y = 30.0       # Distance from top/bottom edges
pair_spacing = 30.0   # Vertical distance between the two holes in each corner group

# Calculate coordinate offsets from center
x_offset = (width / 2) - margin_x
y_outer = (height / 2) - margin_y
y_inner = y_outer - pair_spacing

# Define the list of hole centers (x, y)
# There are 4 pairs, one in each corner
pts = [
    # Top-Right Pair
    (x_offset, y_outer), (x_offset, y_inner),
    # Top-Left Pair
    (-x_offset, y_outer), (-x_offset, y_inner),
    # Bottom-Right Pair
    (x_offset, -y_outer), (x_offset, -y_inner),
    # Bottom-Left Pair
    (-x_offset, -y_outer), (-x_offset, -y_inner),
]

# Generate the model
result = (
    cq.Workplane("XY")
    .box(width, height, thickness)  # Create the main rectangular plate
    .faces(">Z")                    # Select the top face
    .workplane()
    .pushPoints(pts)                # Place points for all holes
    .hole(hole_diameter)            # Cut through-holes
)