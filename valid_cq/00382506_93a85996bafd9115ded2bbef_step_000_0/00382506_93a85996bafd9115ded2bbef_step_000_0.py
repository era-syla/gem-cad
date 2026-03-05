import cadquery as cq

# -- Parametric Dimensions --
length = 80.0          # Overall length of the plate
width = 50.0           # Overall width of the plate
thickness = 3.0        # Plate thickness
fillet_radius = 3.0    # Radius for corner fillets
hole_diameter = 3.5    # Diameter of mounting holes
hole_margin = 4.0      # Margin from the edge to hole center
cutout_radius = 8.0    # Radius of the semi-circular cutout

# -- Geometry Construction --

# 1. Create base rectangular plate
result = cq.Workplane("XY").box(length, width, thickness)

# 2. Apply fillets to all vertical corners
result = result.edges("|Z").fillet(fillet_radius)

# 3. Create mounting holes in the corners
# Calculate hole positions relative to center
x_pos = length / 2 - hole_margin
y_pos = width / 2 - hole_margin

hole_locations = [
    (x_pos, y_pos),
    (x_pos, -y_pos),
    (-x_pos, y_pos),
    (-x_pos, -y_pos)
]

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(hole_locations)
    .circle(hole_diameter / 2)
    .cutThruAll()
)

# 4. Create the semi-circular cutout
# Positioned on the left short edge (-X direction), centered on Y
result = (
    result.faces(">Z")
    .workplane()
    .moveTo(-length / 2, 0)
    .circle(cutout_radius)
    .cutThruAll()
)