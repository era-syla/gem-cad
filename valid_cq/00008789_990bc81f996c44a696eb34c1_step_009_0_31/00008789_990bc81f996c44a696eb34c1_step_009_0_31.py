import cadquery as cq

# --- Parameters ---
# Overall plate dimensions
length = 120.0  
width = 80.0    
thickness = 5.0 

# Corner cut (chamfer) dimensions on the top-right
cut_x = 50.0  
cut_y = 40.0  

# Hole dimensions and positions
hole_radius = 5.0
hole_positions = [
    (30.0, 45.0),   # Left hole
    (60.0, 65.0),   # Top hole
    (85.0, 40.0),   # Middle-right hole
    (100.0, 20.0)   # Bottom-right hole
]

# --- Geometry Generation ---
# Define the outer bounding vertices
outer_profile = [
    (0, 0),
    (length, 0),
    (length, width - cut_y),
    (length - cut_x, width),
    (0, width)
]

# Create the 2D profile, add holes, and extrude into 3D
result = (
    cq.Workplane("XY")
    .polyline(outer_profile)
    .close()
    .pushPoints(hole_positions)
    .circle(hole_radius)
    .extrude(thickness)
)