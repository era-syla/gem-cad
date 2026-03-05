import cadquery as cq

# Parametric dimensions based on visual estimation of the provided image
base_diameter = 25.0
base_height = 8.0
base_flat_offset = 10.5  # Distance from center to the flat cut (D-shape profile)

shaft_diameter = 16.0
shaft_length = 140.0

tip_diameter = 12.0
tip_height = 5.0

hole_diameter = 5.0
hole_depth = 20.0

# 1. Create the base cylinder
result = cq.Workplane("XY").circle(base_diameter / 2.0).extrude(base_height)

# 2. Cut the flat side on the base to create the "D" shape
# Calculate the center position for the cutting rectangle so its edge is at base_flat_offset
cut_width = base_diameter
cut_center_x = base_flat_offset + (cut_width / 2.0)

result = (
    result.faces(">Z")
    .workplane()
    .moveTo(cut_center_x, 0)
    .rect(cut_width, base_diameter * 2.0)  # Use a large enough rectangle to clear the geometry
    .cutBlind(-base_height)
)

# 3. Create the long main shaft
result = (
    result.faces(">Z")
    .workplane()
    .circle(shaft_diameter / 2.0)
    .extrude(shaft_length)
)

# 4. Create the stepped-down tip
result = (
    result.faces(">Z")
    .workplane()
    .circle(tip_diameter / 2.0)
    .extrude(tip_height)
)

# 5. Create the center hole at the top
result = (
    result.faces(">Z")
    .workplane()
    .circle(hole_diameter / 2.0)
    .cutBlind(-hole_depth)
)

# 6. Apply a small chamfer to the top edges for a realistic finish
result = result.edges(">Z").chamfer(0.5)