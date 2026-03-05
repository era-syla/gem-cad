import cadquery as cq

# -- Parametric Dimensions --
length = 60.0          # Total length of the base
width = 15.0           # Width of the extrusion
base_height = 10.0     # Height of the rectangular base
total_height = 25.0    # Overall height of the part

# Top arm geometry definitions
arm_tip_x = 18.0       # X position of the top-front edge
nose_setback = 4.0     # Horizontal distance the nose bevels back
nose_y = 17.0          # Y height of the bottom of the nose tip

# Hinge/Neck geometry definitions
neck_top_x = 48.0      # X position where the arm underside meets the neck
neck_top_y = 14.0      # Y height where the arm underside meets the neck
neck_base_x = 42.0     # X position where the neck meets the base

# -- Profile Construction --
# Define vertices for the side profile on the XZ plane
# Path traces counter-clockwise starting from origin (0,0)
points = [
    (0, 0),                                     # 1. Base Bottom-Left
    (length, 0),                                # 2. Base Bottom-Right
    (length, total_height),                     # 3. Top-Right Corner (Back of arm)
    (arm_tip_x, total_height),                  # 4. Top-Left Corner (Front of arm)
    (arm_tip_x + nose_setback, nose_y),         # 5. Nose Tip (Bottom of front bevel)
    (neck_top_x, neck_top_y),                   # 6. Top of the hinge/throat (underside)
    (neck_base_x, base_height),                 # 7. Bottom of the hinge/throat (on base)
    (0, base_height)                            # 8. Base Top-Left
]

# -- Model Generation --
# Create sketch on XZ plane and extrude along Y
result = (
    cq.Workplane("XZ")
    .polyline(points)
    .close()
    .extrude(width)
)