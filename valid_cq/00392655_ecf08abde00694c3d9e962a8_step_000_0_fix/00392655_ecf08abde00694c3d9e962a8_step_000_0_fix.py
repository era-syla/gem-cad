import cadquery as cq

# Parameters
hub_size = 8.0
arm_width = 3.0
arm_length = 20.0
ring_outer_d = 8.0
ring_inner_d = 4.0
thickness = 2.0

# Central hub
result = cq.Workplane("XY").rect(hub_size, hub_size).extrude(thickness)

# Add six arms
for angle in range(0, 360, 60):
    arm = (
        cq.Workplane("XY")
        .transformed(offset=(0, hub_size/2 + arm_length/2, 0), rotate=(0, 0, angle))
        .rect(arm_width, arm_length)
        .extrude(thickness)
    )
    result = result.union(arm)

# Add rings at the end of each arm
for angle in range(0, 360, 60):
    ring = (
        cq.Workplane("XY")
        .transformed(offset=(0, hub_size/2 + arm_length, 0), rotate=(0, 0, angle))
        .circle(ring_outer_d/2)
        .circle(ring_inner_d/2)
        .extrude(thickness)
    )
    result = result.union(ring)