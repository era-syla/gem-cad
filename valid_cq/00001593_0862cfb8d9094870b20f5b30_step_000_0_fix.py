import cadquery as cq

# Main box dimensions
box_length = 80
box_width = 40
box_height = 30

# Create the main body
body = cq.Workplane("XY").box(box_length, box_width, box_height)

# Add feet/tabs at the bottom corners on the short sides
# Left side feet (at x = -box_length/2)
foot_width = 4
foot_height = 4
foot_depth = 8

# Create feet on the left side (negative x)
left_foot1 = (cq.Workplane("XY")
    .center(-box_length/2 - foot_depth/2, -box_width/4)
    .box(foot_depth, foot_width, foot_height)
    .translate((0, 0, -box_height/2 + foot_height/2))
)

left_foot2 = (cq.Workplane("XY")
    .center(-box_length/2 - foot_depth/2, box_width/4)
    .box(foot_depth, foot_width, foot_height)
    .translate((0, 0, -box_height/2 + foot_height/2))
)

# Create feet on the right side (positive x)
right_foot1 = (cq.Workplane("XY")
    .center(box_length/2 + foot_depth/2, -box_width/4)
    .box(foot_depth, foot_width, foot_height)
    .translate((0, 0, -box_height/2 + foot_height/2))
)

right_foot2 = (cq.Workplane("XY")
    .center(box_length/2 + foot_depth/2, box_width/4)
    .box(foot_depth, foot_width, foot_height)
    .translate((0, 0, -box_height/2 + foot_height/2))
)

# Create pins/tabs protruding from the front face (negative y side)
# These are the horizontal pins visible on the front
pin_length = 12
pin_width = 3
pin_height = 3
pin_z = 0  # middle height

# Pins on the front face (negative y)
pin_positions_x = [-box_length/4, 0, box_length/4]

pins = cq.Workplane("XY")
for px in pin_positions_x:
    pin = (cq.Workplane("XY")
        .center(px, -box_width/2 - pin_length/2)
        .box(pin_width, pin_length, pin_height)
        .translate((0, 0, pin_z))
    )
    pins = pins.union(pin)

# Combine everything
result = body.union(left_foot1).union(left_foot2).union(right_foot1).union(right_foot2).union(pins)