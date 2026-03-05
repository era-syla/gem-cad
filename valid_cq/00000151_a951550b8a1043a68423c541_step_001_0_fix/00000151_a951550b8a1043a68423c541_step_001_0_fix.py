import cadquery as cq

# Parameters
head_width = 18
head_depth = 12
head_height = 10
pin_diameter = 8
pin_length = 35
groove_depth = 1
groove_width = 2
fillet_radius = 2.5

# Build the head (rectangular block with fillets)
head = (
    cq.Workplane("XY")
    .box(head_width, head_depth, head_height)
    .translate((0, 0, pin_length + head_height / 2))
)

# Apply fillets to head edges
head = (
    cq.Workplane("XY")
    .box(head_width, head_depth, head_height)
    .edges("|Z")
    .fillet(fillet_radius)
    .edges(">Z")
    .fillet(fillet_radius)
    .translate((0, 0, pin_length + head_height / 2))
)

# Build the pin (cylinder)
pin = (
    cq.Workplane("XY")
    .cylinder(pin_length, pin_diameter / 2)
    .translate((0, 0, pin_length / 2))
)

# Build the retention groove near the bottom of the pin
groove_z = groove_width + 2
groove = (
    cq.Workplane("XY")
    .cylinder(groove_width, pin_diameter / 2 - groove_depth + 0.5)
    .translate((0, 0, groove_z))
)

# Create the pin with groove
pin_with_groove = (
    cq.Workplane("XY")
    .cylinder(pin_length, pin_diameter / 2)
    .cut(
        cq.Workplane("XY")
        .circle(pin_diameter / 2 + 0.1)
        .circle(pin_diameter / 2 - groove_depth)
        .extrude(groove_width)
        .translate((0, 0, groove_z - groove_width / 2))
    )
    .translate((0, 0, pin_length / 2))
)

# Position the head on top of the pin
# The head should sit on top of the pin
# Pin goes from z=0 to z=pin_length
# Head center at z = pin_length + head_height/2

head_solid = (
    cq.Workplane("XY")
    .box(head_width, head_depth, head_height)
    .edges("|Z")
    .fillet(fillet_radius)
    .edges(">Z")
    .fillet(fillet_radius)
    .translate((0, -head_depth / 4, pin_length + head_height / 2))
)

# Combine pin and head
result = pin_with_groove.union(head_solid)

# Add a small cylinder at the very bottom tip
tip = (
    cq.Workplane("XY")
    .cylinder(2, pin_diameter / 2 - 1)
    .translate((0, 0, 1))
)

result = result.union(tip)