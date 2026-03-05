import cadquery as cq

# Dimensions and Parameters
length = 100.0          # Total length of the hinge leaf
width = 35.0            # Width of the leaf
thickness = 2.5         # Thickness of the material
pin_radius = 2.0        # Radius of the hinge pin
knuckle_radius = pin_radius + thickness # Outer radius of the knuckle
pin_extension = 30.0    # Length the pin extends out

# Feature parameters
num_knuckles = 3        # Number of knuckles on this leaf (implies 5 zones total)
notch_width = 8.0
notch_depth = 3.5
hole_size = 5.0
hole_margin = 3.0

# 1. Create the Hinge Pin
# A cylinder extending beyond the hinge body
pin = (
    cq.Workplane("YZ")
    .circle(pin_radius)
    .extrude(length + pin_extension)
    .translate((-pin_extension, 0, knuckle_radius))
)

# 2. Create the Base Leaf
# A flat rectangular plate
leaf = (
    cq.Workplane("XY")
    .box(length, width, thickness, centered=False)
)

# 3. Create the Knuckle Cylinder
# Full length cylinder initially, will be cut later
knuckle_cylinder = (
    cq.Workplane("YZ")
    .circle(knuckle_radius)
    .extrude(length)
    .translate((0, 0, knuckle_radius))
)

# Combine Leaf and Knuckle into one body
body = leaf.union(knuckle_cylinder)

# 4. Cut the Pin Hole
# Create a hole through the knuckle for the pin (with slight clearance)
hole_clearance = 0.1
pin_hole = (
    cq.Workplane("YZ")
    .circle(pin_radius + hole_clearance)
    .extrude(length)
    .translate((0, 0, knuckle_radius))
)
body = body.cut(pin_hole)

# 5. Cut Knuckle Gaps
# We assume a pattern of 5 zones: Knuckle, Gap, Knuckle, Gap, Knuckle
num_zones = 5
zone_length = length / num_zones
# Cut zones 1 and 3 (0-indexed)
for i in [1, 3]:
    gap_center_x = (i * zone_length) + (zone_length / 2.0)
    
    # Cutter box must be large enough to remove the knuckle section
    gap_cutter = (
        cq.Workplane("XY")
        .workplane(offset=knuckle_radius)
        .center(gap_center_x, 0)
        .box(zone_length, knuckle_radius * 2.2, knuckle_radius * 2.2)
    )
    body = body.cut(gap_cutter)

# 6. Create Edge Notches and Square Holes
# Pattern: Tooth, Notch, Tooth, Notch... 
# Calculate spacing for 5 teeth and 4 notches
tooth_width = (length - 4 * notch_width) / 5.0
current_x = tooth_width

for _ in range(4):
    # --- Cut Notch ---
    notch_center_x = current_x + (notch_width / 2.0)
    notch_cutter = (
        cq.Workplane("XY")
        .workplane(offset=thickness / 2.0)
        .center(notch_center_x, width)
        .box(notch_width, notch_depth * 2.0, thickness * 2.0)
    )
    body = body.cut(notch_cutter)
    
    # --- Cut Square Hole ---
    # Aligned with notch in X, offset in Y
    hole_y = width - notch_depth - hole_margin - (hole_size / 2.0)
    hole_cutter = (
        cq.Workplane("XY")
        .center(notch_center_x, hole_y)
        .rect(hole_size, hole_size)
        .extrude(thickness * 2.0) # Ensure cut through
        .translate((0, 0, -thickness/2.0))
    )
    body = body.cut(hole_cutter)
    
    # Advance X position
    current_x += notch_width + tooth_width

# 7. Final Assembly
# Union the body with the pin
result = body.union(pin)