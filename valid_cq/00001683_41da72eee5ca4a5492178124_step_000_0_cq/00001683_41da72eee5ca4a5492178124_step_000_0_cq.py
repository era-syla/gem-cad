import cadquery as cq

# --- Parametric Dimensions ---
length = 100.0   # Length of the square plate
width = 100.0    # Width of the square plate
thickness = 10.0 # Thickness of the plate
corner_radius = 5.0 # Radius for the corners of the square profile
edge_fillet = 2.0   # Radius for filleting the top and bottom edges

# --- 3D Modeling ---

# 1. Create the base box
# 2. Fillet the vertical edges to create rounded corners
# 3. Fillet the top and bottom edges for the smooth finish seen in the image

result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .edges("|Z")  # Select vertical edges
    .fillet(corner_radius)
    .edges("#Z")  # Select edges perpendicular to Z (top and bottom perimeters)
    .fillet(edge_fillet)
)

# If running in an environment that requires showing the object
# show_object(result)