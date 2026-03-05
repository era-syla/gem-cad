import cadquery as cq

# --- Parametric Definitions ---
height = 800.0        # Total height of the plate
width = 150.0         # Total width of the plate
thickness = 5.0       # Thickness of the plate
hole_diameter = 8.0   # Diameter of the mounting holes
num_rows = 16         # Number of holes along the vertical edge
edge_margin = 15.0    # Distance from hole center to the nearest edge

# --- Calculations ---
# Calculate the spacing between the two columns of holes
# x_spacing is the distance between the centers of the left and right columns
col_spacing = width - (2 * edge_margin)

# Calculate the vertical pitch (spacing between rows)
# The holes span from -y to +y, leaving the margin at top and bottom
# Total vertical span for holes = height - 2 * margin
row_spacing = (height - (2 * edge_margin)) / (num_rows - 1)

# --- Geometry Construction ---
result = (
    cq.Workplane("XY")
    # Create the base rectangular plate
    .box(width, height, thickness)
    # Select the top face to place holes
    .faces(">Z")
    .workplane()
    # Create a rectangular array of points for the holes
    # 2 columns, 'num_rows' rows
    .rarray(col_spacing, row_spacing, 2, num_rows)
    # Cut holes at the array points
    .hole(hole_diameter)
)