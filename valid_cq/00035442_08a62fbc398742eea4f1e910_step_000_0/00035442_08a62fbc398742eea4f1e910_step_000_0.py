import cadquery as cq

# Parametric dimensions for the cross shape
overall_height = 100.0  # Total length of the vertical arm
overall_width = 100.0   # Total length of the horizontal arm
arm_width = 25.0        # Width of the arms
thickness = 5.0         # Thickness of the plate

# Create the vertical arm centered at the origin
vertical_arm = cq.Workplane("XY").box(arm_width, overall_height, thickness)

# Create the horizontal arm centered at the origin
horizontal_arm = cq.Workplane("XY").box(overall_width, arm_width, thickness)

# Combine the two arms into a single solid using a boolean union
result = vertical_arm.union(horizontal_arm)