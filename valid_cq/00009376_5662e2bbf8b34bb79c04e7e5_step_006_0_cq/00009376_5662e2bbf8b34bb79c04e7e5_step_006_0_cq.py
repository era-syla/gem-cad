import cadquery as cq

# Parametric dimensions
# Main body (top cylinder)
head_diameter = 10.0
head_height = 30.0

# Pin/Shaft (bottom cylinder)
pin_diameter = 2.0
pin_length = 20.0

# Create the head (larger cylinder)
# We center it on XY plane, extending upwards in Z
head = cq.Workplane("XY").circle(head_diameter / 2.0).extrude(head_height)

# Create the pin (smaller cylinder)
# It extends downwards from the bottom of the head
pin = (
    cq.Workplane("XY")
    .circle(pin_diameter / 2.0)
    .extrude(-pin_length)  # Negative extrusion to go downwards
)

# Combine the two parts into a single object
result = head.union(pin)

# Export or display the result (for validation purposes, though not strictly required by prompt)
if "show_object" in locals():
    show_object(result)