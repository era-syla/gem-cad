import cadquery as cq

# Main bar dimensions
bar_length = 200
bar_width = 10
bar_height = 4

# Create the main horizontal bar
main_bar = (
    cq.Workplane("XY")
    .box(bar_length, bar_width, bar_height)
)

# Left end plate (wider/taller section)
left_plate_width = 30
left_plate_depth = 20
left_plate_height = 6

left_plate = (
    cq.Workplane("XY")
    .box(left_plate_width, left_plate_depth, left_plate_height)
    .translate((-bar_length/2 + left_plate_width/2, 0, (left_plate_height - bar_height)/2))
)

# Right end plate
right_plate_width = 30
right_plate_depth = 20
right_plate_height = 6

right_plate = (
    cq.Workplane("XY")
    .box(right_plate_width, right_plate_depth, right_plate_height)
    .translate((bar_length/2 - right_plate_width/2, 0, (right_plate_height - bar_height)/2))
)

# Notches on left plate - step cutout
left_notch = (
    cq.Workplane("XY")
    .box(8, 8, left_plate_height + 2)
    .translate((-bar_length/2 + left_plate_width - 4, left_plate_depth/2 - 4, (left_plate_height - bar_height)/2))
)

# Right notch
right_notch = (
    cq.Workplane("XY")
    .box(8, 8, right_plate_height + 2)
    .translate((bar_length/2 - right_plate_width + 4, -left_plate_depth/2 + 4, (right_plate_height - bar_height)/2))
)

# Combine main parts
combined = main_bar.union(left_plate).union(right_plate)

# Cut notches to create step profiles on ends
combined = combined.cut(left_notch).cut(right_notch)

# Add small cylindrical hinge/connector detail in the middle
hinge1 = (
    cq.Workplane("XY")
    .cylinder(bar_width, 3)
    .translate((0, 0, bar_height/2 + bar_width/2))
)

# Small sphere-like detail
hinge_detail = (
    cq.Workplane("XY")
    .sphere(3)
    .translate((0, 0, bar_height/2))
)

# Small cylinders around center joint
joint_cyl1 = (
    cq.Workplane("XY")
    .cylinder(6, 2)
    .translate((-5, 0, bar_height/2))
)

joint_cyl2 = (
    cq.Workplane("XY")
    .cylinder(6, 2)
    .translate((5, 0, bar_height/2))
)

joint_cyl3 = (
    cq.Workplane("XY")
    .cylinder(6, 2)
    .translate((0, 0, bar_height/2))
)

combined = combined.union(joint_cyl1).union(joint_cyl2).union(joint_cyl3)

result = combined