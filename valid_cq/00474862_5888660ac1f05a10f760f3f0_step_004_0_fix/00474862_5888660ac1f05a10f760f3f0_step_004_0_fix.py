import cadquery as cq

# Parameters for the model
tube_length = 100.0
tube_diameter = 10.0
joint_diameter = 15.0
joint_thickness = 5.0

# Create the main tube
tube = cq.Workplane("front").circle(tube_diameter / 2).extrude(tube_length)

# Create the joint at one end
joint = (
    cq.Workplane("front")
    .circle(joint_diameter / 2)
    .extrude(joint_thickness)
    .edges(">Z")
    .chamfer(1.0)
)

# Position the joint at the end of the tube
result = tube.union(joint.translate((0, 0, tube_length)))

# Mirror to create the symmetrical part
result = result.union(result.mirror("YZ"))

# Adding more features could be done similarly
# Example for adding another element might be:
additional_tube = cq.Workplane("front").circle(tube_diameter / 2).extrude(tube_length / 2)
result = result.union(additional_tube.translate((0, tube_diameter, tube_length / 2)))

result
