import cadquery as cq

# --- Parameters ---
# Overall plate dimensions
L = 300.0             # Total length of the plate
H_left = 70.0         # Height of the left section
H_right = 100.0       # Height of the right section
thickness = 10.0      # Plate thickness
step_pos = 175.0      # X-position of the vertical step transition

# Feature dimensions
hole_size = 22.0      # Side length of square holes
hole_margin_top = 25.0  # Distance from top edge to center of square holes
tri_size = 12.0       # Side length of triangular markers
tri_margin_top = 55.0 # Distance from top edge to center of triangular markers

# --- Geometry Generation ---

# 1. Base Plate Profile
# Defined in the XY plane, with (0,0) at the top-left corner
# Y-axis is negative downwards
pts = [
    (0, 0),                  # Top-left
    (L, 0),                  # Top-right
    (L, -H_right),           # Bottom-right
    (step_pos, -H_right),    # Step inner corner
    (step_pos, -H_left),     # Step outer corner
    (0, -H_left)             # Bottom-left
]

# Create the base solid
result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(thickness)
)

# 2. Square Holes
# Holes are positioned horizontally at approx 20%, 50%, and 80% of length
hole_x_positions = [L * 0.2, L * 0.5, L * 0.8]
hole_centers = [(x, -hole_margin_top) for x in hole_x_positions]

result = (
    result.faces(">Z")
    .workplane(centerOption="ProjectedOrigin")
    .pushPoints(hole_centers)
    .rect(hole_size, hole_size)
    .cutThruAll()
)

# 3. Triangular Markers
# Triangles are located under each hole and at the midpoints between holes
tri_x_positions = []
# Add positions under holes and midpoints
tri_x_positions.append(hole_x_positions[0])                         # Under Hole 1
tri_x_positions.append((hole_x_positions[0] + hole_x_positions[1]) / 2) # Between 1 & 2
tri_x_positions.append(hole_x_positions[1])                         # Under Hole 2
tri_x_positions.append((hole_x_positions[1] + hole_x_positions[2]) / 2) # Between 2 & 3
tri_x_positions.append(hole_x_positions[2])                         # Under Hole 3

tri_centers = [(x, -tri_margin_top) for x in tri_x_positions]

# Helper calculations for an equilateral triangle pointing down
# Height h = side * sqrt(3) / 2
h_tri = tri_size * 0.866025
dy_top = h_tri / 2.0
dy_bot = -h_tri / 2.0
dx = tri_size / 2.0

# Cut each triangle individually to ensure correct orientation (pointing down)
for cx, cy in tri_centers:
    # Define vertices relative to the center point
    p1 = (cx - dx, cy + dy_top) # Top Left
    p2 = (cx + dx, cy + dy_top) # Top Right
    p3 = (cx, cy + dy_bot)      # Bottom Tip (Apex)
    
    result = (
        result.faces(">Z")
        .workplane(centerOption="ProjectedOrigin")
        .polyline([p1, p2, p3])
        .close()
        .cutThruAll()
    )