import cadquery as cq

# Parameters
thickness = 5.0
arm_width = 10.0
leg_width = 15.0
arm_length = 80.0
leg_height = 20.0

# Define 2D profile of bracket
profile_pts = [
    (0, 0),
    (leg_height, 0),
    (leg_height + arm_length, 0),
    (leg_height + arm_length, arm_width),
    (leg_height, arm_width),
    (leg_height, leg_width),
    (0, leg_width)
]

# Create base solid by extruding the profile
result = (
    cq.Workplane("XY")
      .polyline(profile_pts)
      .close()
      .extrude(thickness)
)

# Hole positions
tip_hole_pos   = (leg_height + arm_length - 10.0, arm_width / 2.0)
mid1_hole_pos  = (leg_height + arm_length * 1.0/3.0, arm_width / 2.0)
mid2_hole_pos  = (leg_height + arm_length * 2.0/3.0, arm_width / 2.0)
leg_hole_pos   = (leg_height / 2.0, leg_width / 2.0)

# Hole diameters
hole_dia_arm = 4.0
hole_dia_leg = 6.0

# Drill holes through thickness on the top face
result = (
    result.faces(">Z")
      .workplane()
      .pushPoints([tip_hole_pos])
      .hole(hole_dia_arm)
      .pushPoints([mid1_hole_pos, mid2_hole_pos])
      .hole(hole_dia_arm)
      .pushPoints([leg_hole_pos])
      .hole(hole_dia_leg)
)

# Fillet all edges
result = result.edges().fillet(1.0)