import cadquery as cq

# --- Parameters ---
# Dimensions estimated from standard mending plate sizes
num_holes = 7
hole_spacing = 20.0      # Distance between hole centers
width = 20.0             # Width of the plate
thickness = 3.0          # Thickness of the plate
end_margin = 10.0        # Distance from last hole center to plate end
chamfer_size = 4.0       # Size of corner cuts

# Hole specifications (Countersunk)
hole_diameter = 5.5      # Through hole diameter (clearance for M5)
csk_diameter = 10.0      # Diameter of the countersink at the surface
csk_angle = 90.0         # Angle of the countersink cone

# --- Calculation ---
# Total length derived from hole count and spacing
total_length = ((num_holes - 1) * hole_spacing) + (2 * end_margin)

# Generate list of (x, y) coordinates for the holes centered on the part
# The layout is symmetric around the origin (0,0)
x_start = -((num_holes - 1) * hole_spacing) / 2
hole_locations = [(x_start + i * hole_spacing, 0) for i in range(num_holes)]

# --- Geometry Generation ---
result = (
    cq.Workplane("XY")
    # 1. Create the base rectangular bar
    .box(total_length, width, thickness)
    
    # 2. Apply chamfers to the four vertical corners
    .edges("|Z")
    .chamfer(chamfer_size)
    
    # 3. Create countersunk holes on the top face
    .faces(">Z")
    .workplane()
    .pushPoints(hole_locations)
    .cskHole(hole_diameter, csk_diameter, csk_angle)
)