import cadquery as cq

# Parametric dimensions
head_diameter = 10.0
head_height = 5.0
shaft_diameter = 6.0
shaft_length = 35.0

# Create the head of the pin
# We start by drawing a circle on the XY plane and extruding it
head = cq.Workplane("XY").circle(head_diameter / 2).extrude(head_height)

# Create the shaft of the pin
# We select the top face of the head and draw the shaft circle
# Alternatively, we can draw it on the same plane and extrude further, 
# but building on faces is more idiomatic for "stacking" parts.
# Here, to keep it simple and aligned, we can extrude from the "bottom" face 
# or just start a new extrusion from the same plane but in the opposite direction 
# or just stack them. Let's stack them for clarity.

result = (
    cq.Workplane("XY")
    .circle(head_diameter / 2)
    .extrude(head_height)
    .faces(">Z")
    .workplane()
    .circle(shaft_diameter / 2)
    .extrude(shaft_length)
)

# Alternatively, a single revolve operation could be used, but two extrusions 
# are very readable for this simple shape.