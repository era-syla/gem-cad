import cadquery as cq

# --- Parameters ---
plate_height = 400.0  # Total height of the plate
plate_width = 100.0   # Total width of the plate
thickness = 5.0       # Thickness of the plate
corner_radius = 5.0   # Radius for rounded corners

# Hole parameters
hole_diameter = 4.0   # Diameter of the mounting holes
hole_margin_x = 10.0  # Distance from side edges
hole_margin_y = 10.0  # Distance from top/bottom edges
mid_hole_spacing = 50.0 # Spacing between the two middle holes

# --- Geometry Construction ---

# 1. Create the base plate with rounded corners
# We start with a box and apply fillets to the vertical edges
result = (
    cq.Workplane("XY")
    .box(plate_width, plate_height, thickness)
    .edges("|Z")
    .fillet(corner_radius)
)

# 2. Define Hole Locations
# Top holes (two of them)
top_y = plate_height / 2 - hole_margin_y
# Bottom holes (two of them)
bottom_y = -(plate_height / 2 - hole_margin_y)

# Side locations relative to center
left_x = -(plate_width / 2 - hole_margin_x)
right_x = (plate_width / 2 - hole_margin_x)

# Middle holes (two on the left side)
mid_y_upper = mid_hole_spacing / 2
mid_y_lower = -mid_hole_spacing / 2


# List of (x, y) coordinates for all holes
hole_locations = [
    # Top left and right
    (left_x, top_y),
    (right_x, top_y),
    
    # Bottom left and right
    (left_x, bottom_y),
    (right_x, bottom_y),

    # Middle left side holes
    (left_x, mid_y_upper),
    (left_x, mid_y_lower),
]

# 3. Cut the holes
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(hole_locations)
    .hole(hole_diameter)
)

# Return the final object
if 'show_object' in globals():
    show_object(result)