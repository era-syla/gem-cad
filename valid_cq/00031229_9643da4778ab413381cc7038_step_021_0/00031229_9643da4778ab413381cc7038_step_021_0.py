import cadquery as cq

# --- Parameters ---
# Overall dimensions
width = 100.0
height = 80.0
thickness = 10.0

# Feature dimensions
cutout_radius = 35.0   # Radius of the circular cutouts on top/bottom
cutout_depth = 12.0    # How deep the cutout goes into the plate
corner_radius = 6.0    # Fillet radius for the four corners
hole_diameter = 8.0    # Diameter of the through holes
hole_spacing_x = 75.0  # Horizontal distance between hole centers
hole_spacing_y = 55.0  # Vertical distance between hole centers

# --- Geometry Construction ---

# 1. Create the base rectangular plate centered at the origin
result = cq.Workplane("XY").box(width, height, thickness)

# 2. Create and subtract the top and bottom circular cutouts
# Calculate the Y-position for the center of the cutting circles.
# To achieve the "concave" cut, the circle center is placed outside the plate boundary.
# Center Y = (Half Height - Depth) + Radius
cutout_center_y = (height / 2.0 - cutout_depth) + cutout_radius

# Create the top cutting cylinder
top_cutter = (
    cq.Workplane("XY")
    .moveTo(0, cutout_center_y)
    .circle(cutout_radius)
    .extrude(thickness * 2)       # Ensure it cuts through the full thickness
    .translate((0, 0, -thickness)) # Center vertically relative to the plate
)

# Create the bottom cutting cylinder
bottom_cutter = (
    cq.Workplane("XY")
    .moveTo(0, -cutout_center_y)
    .circle(cutout_radius)
    .extrude(thickness * 2)
    .translate((0, 0, -thickness))
)

# Apply the cuts
result = result.cut(top_cutter).cut(bottom_cutter)

# 3. Apply fillets to the four vertical corner edges
# We select edges parallel to the Z-axis. Since the cutouts are in the middle, 
# the original corner edges of the box are preserved and can be selected easily.
# We use a filter to ensure we only grab the outer corners if the cut geometry is complex.
result = result.edges("|Z").filter(lambda e: abs(e.Center().x) > width/4).fillet(corner_radius)

# 4. Create the four mounting holes
# Calculate offsets
hx = hole_spacing_x / 2.0
hy = hole_spacing_y / 2.0

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([
        (hx, hy), 
        (hx, -hy), 
        (-hx, hy), 
        (-hx, -hy)
    ])
    .hole(hole_diameter)
)