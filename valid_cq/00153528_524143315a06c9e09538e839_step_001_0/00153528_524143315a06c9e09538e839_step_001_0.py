import cadquery as cq

# --- Parametric Dimensions ---
height = 100.0
width_bottom = 85.0
width_top = 50.0
thickness = 2.5
corner_fillet = 8.0

# Central large hole parameters
center_hole_dia = 12.0
center_hole_y = 70.0  # Distance from bottom edge

# Mounting holes parameters
mount_hole_dia = 4.0
mount_spacing_x = 31.0  # Horizontal distance between holes
mount_spacing_y = 31.0  # Vertical distance between holes

# --- 3D Model Construction ---

# Define the trapezoidal profile points (counter-clockwise)
# Origin is at the bottom center of the plate
pts = [
    (-width_bottom / 2.0, 0),
    (width_bottom / 2.0, 0),
    (width_top / 2.0, height),
    (-width_top / 2.0, height)
]

# Create the base solid
result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(thickness)
)

# Apply fillets to the top two corners
# Select vertical edges (|Z) that are at the top of the part (>Y)
result = result.edges("|Z").edges(">Y").fillet(corner_fillet)

# Create the central large hole
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(0, center_hole_y)])
    .hole(center_hole_dia)
)

# Calculate mounting hole positions relative to the global coordinate system
dx = mount_spacing_x / 2.0
dy = mount_spacing_y / 2.0

mount_locations = [
    (dx, center_hole_y + dy),
    (dx, center_hole_y - dy),
    (-dx, center_hole_y + dy),
    (-dx, center_hole_y - dy),
]

# Create the mounting holes
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(mount_locations)
    .hole(mount_hole_dia)
)