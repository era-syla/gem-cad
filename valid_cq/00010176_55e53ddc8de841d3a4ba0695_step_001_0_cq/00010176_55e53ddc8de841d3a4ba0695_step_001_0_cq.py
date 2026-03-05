import cadquery as cq

# --- Parametric Dimensions ---
plate_length = 200.0  # Total length of the plate
plate_width = 100.0   # Total width of the plate
plate_thickness = 5.0 # Thickness of the plate

hex_radius = 12.0     # Radius of each hexagon (center to vertex)
hex_spacing = 5.0     # Wall thickness between hexagons

# --- Helper Calculations for Hex Grid ---
# Distance between centers of adjacent hexagons in X (horizontal)
# In a tight packing, center-to-center is sqrt(3) * radius
dx = (hex_radius * 2 * 0.866025) + hex_spacing # cos(30) ~ 0.866

# Distance between centers of rows in Y (vertical)
# Center-to-center vertical is 1.5 * radius
dy = (hex_radius * 1.5) + (hex_spacing * 0.866025)

# --- Geometry Construction ---

# 1. Create the base plate
plate = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# 2. Define the hexagon shape for cutting
# We create a single hexagon sketch that we will reuse
hexagon = (
    cq.Workplane("XY")
    .polygon(nSides=6, diameter=hex_radius * 2)
    .extrude(plate_thickness * 2) # Make it long enough to cut through
)

# 3. Create the grid points
# We need to calculate a grid of points. Since the image shows a staggered
# honeycomb pattern, every other row is shifted.

points = []
# Estimate number of rows and columns based on dimensions
num_cols = int(plate_length / dx) 
num_rows = int(plate_width / dy) 

# Center the pattern
start_x = -((num_cols - 1) * dx) / 2
start_y = -((num_rows - 1) * dy) / 2

for row in range(num_rows):
    for col in range(num_cols):
        # Calculate x and y positions
        x_pos = start_x + (col * dx)
        y_pos = start_y + (row * dy)
        
        # Shift every odd row to create the honeycomb staggering
        if row % 2 == 1:
            x_pos += dx / 2
            
        # Optional: Check if the point is within a margin of the plate edges
        # to ensure the cut is fully contained or looks nice.
        margin = hex_radius + 5
        if (abs(x_pos) < (plate_length / 2 - margin) and 
            abs(y_pos) < (plate_width / 2 - margin)):
            points.append((x_pos, y_pos))

# 4. Perform the cut
# We create a workplane on the top face, push all our calculated points,
# draw the hexagon at each point, and do a cut.
result = (
    plate.faces(">Z").workplane()
    .pushPoints(points)
    .polygon(nSides=6, diameter=hex_radius * 2)
    .cutThruAll()
)

# Export or display is handled by the environment, but 'result' is the final object.