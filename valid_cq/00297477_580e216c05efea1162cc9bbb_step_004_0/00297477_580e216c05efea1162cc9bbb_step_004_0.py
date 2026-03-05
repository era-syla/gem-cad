import cadquery as cq

# --- Parametric Dimensions ---
# Overall dimensions of the plate
plate_width_bottom = 320.0    # Width at the bottom edge
plate_depth = 200.0           # Total height/depth (Y-axis distance)
plate_width_top = 140.0       # Width at the top edge
side_straight_height = 40.0   # Height of the vertical straight sections on the sides
plate_thickness = 4.0         # Thickness of the material

# Slot dimensions
slot_width = 50.0
slot_height = 6.0
slot_y_offset = 15.0          # Distance from bottom edge to center of slot

# Hole parameters
hole_diameter = 3.0
num_holes_angled_side = 5     # Number of holes along the long angled edge
num_holes_top = 3             # Number of holes along the top edge
num_holes_vertical_side = 2   # Number of holes along the short vertical side

# --- Helper Function ---
def generate_points_on_segment(start_pt, end_pt, count):
    """
    Generates a list of (x, y) points evenly distributed along a line segment,
    inset from the endpoints to avoid corners.
    """
    points = []
    if count < 1:
        return points
    
    x1, y1 = start_pt
    x2, y2 = end_pt
    
    # Calculate spacing. We use (count + 1) divisions to space them evenly
    # between the endpoints without touching the endpoints.
    for i in range(count):
        t = (i + 1) / (count + 1)
        px = x1 + (x2 - x1) * t
        py = y1 + (y2 - y1) * t
        points.append((px, py))
    return points

# --- Geometry Definition ---

# Define the vertices of the polygon relative to the global origin (0,0)
# We align the bottom edge with the X-axis, centered on X=0.
v_bottom_right = (plate_width_bottom / 2.0, 0.0)
v_side_right   = (plate_width_bottom / 2.0, side_straight_height)
v_top_right    = (plate_width_top / 2.0, plate_depth)
v_top_left     = (-plate_width_top / 2.0, plate_depth)
v_side_left    = (-plate_width_bottom / 2.0, side_straight_height)
v_bottom_left  = (-plate_width_bottom / 2.0, 0.0)

# Create the main body
base_points = [
    v_bottom_right, 
    v_side_right, 
    v_top_right, 
    v_top_left, 
    v_side_left, 
    v_bottom_left
]

# Extrude the base shape
base = (
    cq.Workplane("XY")
    .polyline(base_points)
    .close()
    .extrude(plate_thickness)
)

# --- Feature Generation ---

# Generate hole coordinates along the perimeter
hole_locations = []
# Right vertical side
hole_locations.extend(generate_points_on_segment(v_bottom_right, v_side_right, num_holes_vertical_side))
# Right angled side
hole_locations.extend(generate_points_on_segment(v_side_right, v_top_right, num_holes_angled_side))
# Top edge
hole_locations.extend(generate_points_on_segment(v_top_right, v_top_left, num_holes_top))
# Left angled side
hole_locations.extend(generate_points_on_segment(v_top_left, v_side_left, num_holes_angled_side))
# Left vertical side
hole_locations.extend(generate_points_on_segment(v_side_left, v_bottom_left, num_holes_vertical_side))

# Create Workplane on the top face
# centerOption="ProjectedOrigin" ensures (0,0) matches the global XY alignment
wp = base.faces(">Z").workplane(centerOption="ProjectedOrigin")

# 1. Cut the rectangular slot
# We move the center to the slot position, cut, and then must move back or account for the shift
result = (
    wp
    .center(0, slot_y_offset)
    .rect(slot_width, slot_height)
    .cutThruAll()
)

# 2. Cut the perimeter holes
# We shift the center back to (0,0) relative to the previous operation
result = (
    result
    .center(0, -slot_y_offset)
    .pushPoints(hole_locations)
    .circle(hole_diameter / 2.0)
    .cutThruAll()
)