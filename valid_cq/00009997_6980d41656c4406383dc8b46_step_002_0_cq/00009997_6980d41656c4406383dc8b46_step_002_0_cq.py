import cadquery as cq

# Parametric dimensions
head_diameter = 20.0
head_height = 5.0
shaft_diameter = 10.0
shaft_length = 30.0
top_circle_diameter = 8.0
top_circle_depth = 0.5 # Shallow cut or indentation for the detail on top

# Create the head
head = cq.Workplane("XY").circle(head_diameter / 2).extrude(head_height)

# Create the shaft
# We start from the bottom face of the head and extrude downwards
shaft = (
    head.faces("<Z")
    .workplane()
    .circle(shaft_diameter / 2)
    .extrude(shaft_length)
)

# Create the top detail (indentation)
# We select the top face of the combined object
result = (
    shaft.faces(">Z")
    .workplane()
    .circle(top_circle_diameter / 2)
    .cutBlind(-top_circle_depth)
)

# Combine into a single object (though extruding from the face usually unions automatically)
# Just making sure result is the final object
# The previous operations chain correctly.

# Export or display
# show_object(result) # This would be used in CQ-editor