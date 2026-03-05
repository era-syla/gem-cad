import cadquery as cq

# --- Parametric Dimensions ---
# Dimensions estimated from visual proportion
head_diameter = 20.0
head_height = 10.0

shaft_diameter = 8.0
shaft_length = 30.0

# --- Modeling ---

# 1. Create the head of the pin/bolt
# Start with a workplane (XY plane) and draw a circle for the head
# Extrude it to create the cylindrical head
head = cq.Workplane("XY").circle(head_diameter / 2).extrude(head_height)

# 2. Create the shaft
# Select the top face of the head to start the shaft
# Draw a smaller circle and extrude it
result = (
    head.faces(">Z")
    .workplane()
    .circle(shaft_diameter / 2)
    .extrude(shaft_length)
)

# Alternatively, you could model this as a single revolved profile,
# but the stacked extrusion method is often more readable for simple shapes.