import cadquery as cq

# --- Parametric Dimensions ---
# Overall dimensions
height = 120.0
width = 50.0
thickness = 15.0

# Hole pattern parameters
hole_diameter = 1.5
hole_col_spacing = 35.0  # Distance between the two columns
hole_start_y = 20.0      # Distance from top edge to first hole
hole_spacing_y = 8.0     # Vertical pitch between holes
num_holes_per_col = 10

# Bottom cutout parameters
cutout_radius = 12.0

# Bottom tab parameters
tab_width = 5.0
tab_height = 3.0
tab_depth = 5.0 # How deep the tab goes into the thickness (or full thickness)

# --- Modeling ---

# 1. Create the main rectangular body
main_body = cq.Workplane("XY").box(width, height, thickness)

# 2. Create the holes
# We need to calculate positions relative to the center of the face
# Center is (0,0) on the XY plane. 
# Top edge is at y = height/2
# Left column x = -hole_col_spacing/2
# Right column x = hole_col_spacing/2

# List of points for the holes
hole_points = []
start_y_coord = (height / 2.0) - hole_start_y

for i in range(num_holes_per_col):
    y_pos = start_y_coord - (i * hole_spacing_y)
    hole_points.append((-hole_col_spacing / 2.0, y_pos))
    hole_points.append((hole_col_spacing / 2.0, y_pos))

# Apply holes to the main body (cutting through Z)
result = (
    main_body
    .faces(">Z")
    .workplane()
    .pushPoints(hole_points)
    .hole(hole_diameter)
)

# 3. Create the bottom semi-circular cutout
# The cutout is at the bottom center (y = -height/2, x = 0)
# We draw a circle on the front face and cut it through
result = (
    result
    .faces(">Z")
    .workplane(centerOption="CenterOfBoundBox")
    .moveTo(0, -height / 2.0)
    .circle(cutout_radius)
    .cutThruAll()
)

# 4. Create the bottom tabs/feet
# The image shows small protrusions at the bottom corners.
# Let's assume they are centered in the thickness.
# Coordinates: y = -height/2 - tab_height/2
# x positions: +/- (width/2 - tab_width/2)

tab_x_offset = (width / 2.0) - (tab_width / 2.0)
tab_y_center = -(height / 2.0) - (tab_height / 2.0)

# Create a temporary solid for the tabs and union it
tabs = (
    cq.Workplane("XY")
    .workplane(offset=-thickness/2 + (thickness-tab_depth)/2) # Adjust Z plane if needed, centered
    .pushPoints([(-tab_x_offset, tab_y_center), (tab_x_offset, tab_y_center)])
    .rect(tab_width, tab_height)
    .extrude(tab_depth)
)

# Since the prompt implies a single solid, let's refine the tab creation.
# Instead of a separate union, let's extrude from the bottom face.

# Alternative approach for tabs to ensure perfect fusion:
# Select bottom face, draw rectangles, extrude.
result = (
    result
    .faces("<Y")
    .workplane()
    .pushPoints([
        (-tab_x_offset, 0), 
        (tab_x_offset, 0)
    ])
    .rect(tab_width, tab_depth) # On the <Y face, X is width, Y is thickness
    .extrude(tab_height)
)

# Final Result
# Re-orient for better viewing match with image (Front view)
# result = result.rotate((0,0,0), (1,0,0), -90)