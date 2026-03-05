import cadquery as cq

# -----------------------------------------------------------------------------
# Parametric Definitions
# -----------------------------------------------------------------------------

# Main Body Dimensions
main_diameter = 12.0
radius = main_diameter / 2.0

# Lengths of the three main cylindrical sections
len_front = 9.0
len_mid = 11.0
len_rear = 9.0

# Groove Dimensions (separating the sections)
groove_width = 0.5
groove_depth = 0.3
groove_radius = radius - groove_depth

# Front Detail
front_chamfer = 1.0

# Rear Detail (Stepped boss and terminal pin)
rear_boss_diameter = 10.5
rear_boss_length = 1.0
pin_width = 3.0
pin_thickness = 1.2
pin_length = 4.0

# -----------------------------------------------------------------------------
# 3D Modeling Construction
# -----------------------------------------------------------------------------

# Initialize workplane on YZ to extrude along X-axis (matches common viewing angles)
# 1. Create the Front Section
result = cq.Workplane("YZ").circle(radius).extrude(len_front)

# 2. Create Groove 1
result = result.faces(">X").workplane().circle(groove_radius).extrude(groove_width)

# 3. Create the Middle Section
result = result.faces(">X").workplane().circle(radius).extrude(len_mid)

# 4. Create Groove 2
result = result.faces(">X").workplane().circle(groove_radius).extrude(groove_width)

# 5. Create the Rear Section
result = result.faces(">X").workplane().circle(radius).extrude(len_rear)

# 6. Apply Chamfer to the Front Face
# Select the face at the minimal X coordinate and apply chamfer
result = result.faces("<X").chamfer(front_chamfer)

# 7. Create Rear Boss
# Select the rear face (max X) and extrude the smaller boss
result = result.faces(">X").workplane().circle(rear_boss_diameter / 2.0).extrude(rear_boss_length)

# 8. Create Rear Pin/Terminal
# Select the new rear face and extrude the rectangular pin
result = (
    result.faces(">X")
    .workplane()
    .rect(pin_width, pin_thickness)
    .extrude(pin_length)
)

# The variable 'result' now contains the final CadQuery object