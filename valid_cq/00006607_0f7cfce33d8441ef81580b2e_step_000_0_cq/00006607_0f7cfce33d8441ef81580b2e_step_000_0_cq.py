import cadquery as cq

# Parametric dimensions
plate_length = 50.0  # Total length of the plate
plate_width_left = 30.0  # Width on the left side (wider side)
plate_width_right = 20.0  # Width on the right side (narrower side)
plate_thickness = 2.0  # Thickness of the main plate
fillet_radius = 3.0    # Radius for corners

boss_diameter = 15.0   # Diameter of the circular protrusion
boss_height = 2.0      # Height of the boss above the plate
boss_x_offset = -5.0   # Position of boss relative to center (shifted left)

# Create the base plate shape
# We'll define points for a polygon to create the tapered shape
pts = [
    (-plate_length/2, -plate_width_left/2),
    (plate_length/2, -plate_width_right/2),
    (plate_length/2, plate_width_right/2),
    (-plate_length/2, plate_width_left/2)
]

# 1. Create the base plate
base_plate = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(plate_thickness)
    .edges("|Z")  # Select vertical edges for filleting
    .fillet(fillet_radius)
)

# 2. Create the circular boss
boss = (
    base_plate.faces(">Z")
    .workplane()
    .center(boss_x_offset, 0)
    .circle(boss_diameter / 2)
    .extrude(boss_height)
)

# Combine into result
result = boss