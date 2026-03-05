import cadquery as cq

# Dimensions and Parameters
plate_length = 100.0   # Dimension along X axis
plate_width = 80.0     # Dimension along Y axis
thickness = 5.0        # Plate thickness
fillet_radius = 8.0    # Radius of rounded corners
hole_diameter = 8.0    # Diameter of mounting holes
hole_spacing = 45.0    # Center-to-center distance between holes
hole_margin = 15.0     # Distance from hole center to the nearest edge

# 1. Create the base plate centered at the origin
result = cq.Workplane("XY").box(plate_length, plate_width, thickness)

# 2. Add fillets to the vertical corners
# Selects all edges parallel to the Z axis
result = result.edges("|Z").fillet(fillet_radius)

# 3. Create the mounting holes
# Position calculation:
# Holes are placed near the negative X edge (left side in standard view)
# x coordinate: Left edge (-length/2) + margin
# y coordinates: Centered around 0, spaced by hole_spacing
x_pos = -(plate_length / 2.0) + hole_margin
hole_points = [
    (x_pos, hole_spacing / 2.0),
    (x_pos, -hole_spacing / 2.0)
]

# Select the top face, push the points, and cut the holes through the solid
result = result.faces(">Z").workplane().pushPoints(hole_points).hole(hole_diameter)