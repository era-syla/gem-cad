import cadquery as cq

# --- Parametric Dimensions ---
length = 150.0          # Total length of the rail
base_width = 8.0        # Width of the narrower bottom section
top_width = 12.0        # Width of the wider top section
base_height = 7.0       # Height of the bottom section
top_height = 4.0        # Height of the top section
hole_diameter = 5.5     # Diameter of the through hole
hole_margin = 10.0      # Distance from the far end to the hole center

# --- Derived Values ---
total_height = base_height + top_height
# Calculate offset to place hole at the far end relative to the face center
# Face center is at length/2. Target is length - margin.
hole_center_offset = (length / 2) - hole_margin

# --- Geometry Construction ---

# Define the points for the T-shaped cross-section
# Profile is drawn on the YZ plane, centered on the Y-axis
profile_points = [
    (-base_width / 2, 0),
    (base_width / 2, 0),
    (base_width / 2, base_height),
    (top_width / 2, base_height),
    (top_width / 2, total_height),
    (-top_width / 2, total_height),
    (-top_width / 2, base_height),
    (-base_width / 2, base_height)
]

# Create the main body and cut the hole
result = (
    cq.Workplane("YZ")
    .polyline(profile_points)
    .close()
    .extrude(length)
    .faces(">Z")                # Select the top face
    .workplane()
    .center(hole_center_offset, 0)
    .hole(hole_diameter)
)