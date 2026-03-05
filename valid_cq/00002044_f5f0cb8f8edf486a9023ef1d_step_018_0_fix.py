import cadquery as cq

# Main body dimensions
body_length = 50
body_width = 25
body_height = 15

# Create main rectangular body (base)
base = (
    cq.Workplane("XY")
    .box(body_length, body_width, body_height)
)

# Create top lid (slightly smaller, sits on top)
lid_height = 3
lid = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, (body_height + lid_height) / 2))
    .box(body_length - 2, body_width - 2, lid_height)
)

# Combine base and lid
main_body = base.union(lid)

# Add connector pins on the front face (left side)
# Series of small rectangular pins
pin_width = 1.5
pin_height = 1.5
pin_depth = 3
num_pins_row = 8
num_rows = 2

pins = cq.Workplane("XY")
first_pin = True

for row in range(num_rows):
    for col in range(num_pins_row):
        x_pos = -body_length / 2 - pin_depth / 2
        y_pos = -body_width / 4 + col * (pin_width + 0.5) - (num_pins_row * (pin_width + 0.5)) / 2 + pin_width
        z_pos = -body_height / 4 + row * (pin_height + 0.5)
        
        pin = (
            cq.Workplane("XY")
            .transformed(offset=(x_pos, y_pos, z_pos))
            .box(pin_depth, pin_width, pin_height)
        )
        if first_pin:
            pins = pin
            first_pin = False
        else:
            pins = pins.union(pin)

main_body = main_body.union(pins)

# Add decorative concentric arc ridges on top surface
# Simulate with thin raised arcs (quarter circles stacked)
arc_base_r = 3
num_arcs = 4

arcs_solid = None
for i in range(num_arcs):
    outer_r = arc_base_r + i * 3
    inner_r = outer_r - 1.5
    arc_height = 0.8
    
    arc = (
        cq.Workplane("XY")
        .transformed(offset=(-body_length / 2 + 8, -body_width / 2 + 8, body_height / 2 + lid_height))
        .cylinder(arc_height, outer_r)
    )
    arc_inner = (
        cq.Workplane("XY")
        .transformed(offset=(-body_length / 2 + 8, -body_width / 2 + 8, body_height / 2 + lid_height))
        .cylinder(arc_height + 0.1, inner_r)
    )
    arc = arc.cut(arc_inner)
    
    # Cut to keep only quarter
    cut_box_x = (
        cq.Workplane("XY")
        .transformed(offset=(-body_length / 2 + 8 - outer_r - 1, -body_width / 2 + 8, body_height / 2 + lid_height))
        .box(outer_r * 2 + 2, outer_r * 2 + 2, arc_height + 1)
    )
    cut_box_y = (
        cq.Workplane("XY")
        .transformed(offset=(-body_length / 2 + 8, -body_width / 2 + 8 - outer_r - 1, body_height / 2 + lid_height))
        .box(outer_r * 2 + 2, outer_r * 2 + 2, arc_height + 1)
    )
    
    arc = arc.cut(cut_box_x).cut(cut_box_y)
    
    if arcs_solid is None:
        arcs_solid = arc
    else:
        arcs_solid = arcs_solid.union(arc)

if arcs_solid is not None:
    main_body = main_body.union(arcs_solid)

# Add a cable on the back right corner
cable_r = 2
cable_length = 20

cable = (
    cq.Workplane("YZ")
    .transformed(offset=(body_width / 2 - 4, body_height / 2 + 1, body_length / 2))
    .cylinder(cable_length, cable_r)
)

# Rotate cable to go diagonally up-right
cable = (
    cq.Workplane("XY")
    .transformed(offset=(body_length / 2 + 5, body_width / 2 - 4, body_height / 2 + 3))
    .cylinder(cable_length, cable_r)
)

main_body = main_body.union(cable)

result = main_body