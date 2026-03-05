import cadquery as cq

# Parametric dimensions for the battery (based on standard AA size)
battery_diameter = 14.5
total_height = 50.5
terminal_diameter = 5.5
terminal_height = 1.5

# Calculate the height of the main cylindrical body
body_height = total_height - terminal_height

# Create the battery geometry
# 1. Start with the main body cylinder on the XY plane
# 2. Select the top face (>Z)
# 3. Draw the terminal circle and extrude it upwards
result = (
    cq.Workplane("XY")
    .circle(battery_diameter / 2.0)
    .extrude(body_height)
    .faces(">Z")
    .workplane()
    .circle(terminal_diameter / 2.0)
    .extrude(terminal_height)
)