import cadquery as cq

# Define dimensions
tube_diameter = 10
tube_length = 100
joint_radius = 12
joint_width = 15

# Create the first tube
tube1 = cq.Workplane("XY").circle(tube_diameter / 2).extrude(tube_length)

# Create a joint at one end
joint1 = (
    cq.Workplane("XY")
    .circle(joint_radius)
    .extrude(joint_width)
    .translate((0, 0, -joint_width))
)

# Create the second tube
tube2 = (
    cq.Workplane("XY")
    .circle(tube_diameter / 2)
    .extrude(tube_length)
    .translate((tube_length, 0, 0))
)

# Create another joint at the end of the second tube
joint2 = (
    cq.Workplane("XY")
    .circle(joint_radius)
    .extrude(joint_width)
    .translate((tube_length, 0, joint_width))
)

# Assemble the components
result = tube1.union(joint1).union(tube2).union(joint2)