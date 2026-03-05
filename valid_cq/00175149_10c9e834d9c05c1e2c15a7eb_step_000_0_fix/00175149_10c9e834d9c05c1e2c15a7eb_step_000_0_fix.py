import cadquery as cq

# Base
base = (cq.Workplane("XY")
        .circle(15)
        .extrude(5))

# Lower arm
lower_arm = (cq.Workplane("XY")
             .workplane(offset=5)
             .center(0, 0)
             .rect(7, 4)
             .extrude(15)
             .edges("|Z")
             .fillet(1))

# Upper arm
upper_arm = (cq.Workplane("XY")
             .workplane(offset=20)
             .center(0, 0)
             .rect(5, 3)
             .extrude(20)
             .edges("|Z")
             .fillet(0.8))

# Forearm
forearm = (cq.Workplane("XY")
           .workplane(offset=40)
           .center(0, 0)
           .rect(3, 2)
           .extrude(10)
           .edges("|Z")
           .fillet(0.5))

# Gripper
gripper = (cq.Workplane("XY")
           .workplane(offset=50)
           .center(0, 0)
           .rect(2, 0.5)
           .extrude(2))

# Assembling the robot arm
result = base.union(lower_arm).union(upper_arm).union(forearm).union(gripper)