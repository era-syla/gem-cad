import cadquery as cq

# --- Parameters ---
length = 8.0
width = 4.0
thickness = 0.2

# Feature dimensions
text_string = "VISHAY"
font_size = 1.5
feature_height = 0.05  # Height of embossed features

# Pads (Right side)
pad_width = 1.2
pad_height = 0.9
pad_x_offset = 2.0  # From center
pad_y_offset = 1.0  # From center

# Markers (Left side)
marker_size = 0.4
marker_x_inner = -1.8
marker_x_outer = -3.0
marker_y_offset = 1.0

# --- Modeling ---

# 1. Create the base plate
base = cq.Workplane("XY").box(length, width, thickness)

# Select the top face for adding features
top_face = base.faces(">Z").workplane()

# 2. Add the text "VISHAY" in the center
# The text() function returns a Workplane object containing the 3D text
text_obj = top_face.text(text_string, fontsize=font_size, distance=feature_height)

# 3. Create the two rectangular pads on the right
pad_locations = [
    (pad_x_offset, pad_y_offset),
    (pad_x_offset, -pad_y_offset)
]

pads = (
    top_face
    .pushPoints(pad_locations)
    .rect(pad_width, pad_height)
    .extrude(feature_height)
)

# 4. Create the four triangular markers on the left
# Define triangle points relative to local center (pointing right)
h = marker_size * 0.866 # Height of equilateral triangle
tri_pts = [
    (h/2, 0),                  # Tip
    (-h/2, marker_size/2),     # Top-left vertex
    (-h/2, -marker_size/2)     # Bottom-left vertex
]

marker_locations = [
    (marker_x_inner, marker_y_offset),
    (marker_x_outer, marker_y_offset),
    (marker_x_inner, -marker_y_offset),
    (marker_x_outer, -marker_y_offset)
]

markers = (
    top_face
    .pushPoints(marker_locations)
    .polyline(tri_pts).close()
    .extrude(feature_height)
)

# --- Final Assembly ---
# Union all separate bodies into one component
result = base.union(text_obj).union(pads).union(markers)