import cadquery as cq

# Parametric dimensions for the stepped pin/shaft
small_shaft_diameter = 2.0
small_shaft_length = 15.0

main_body_diameter = 5.0
main_body_length = 40.0

head_diameter = 6.0
head_length = 5.0

# Create the geometry by stacking cylinders
# We start from the origin and build upwards/along the Z axis, but orienting along an axis is arbitrary.
# Let's align it along the X-axis to match the visual orientation somewhat.

# 1. Create the small shaft (leftmost part)
small_shaft = cq.Workplane("YZ").circle(small_shaft_diameter / 2).extrude(small_shaft_length)

# 2. Create the main body, starting from the end of the small shaft
# We select the face at the far end of the current solid (which is at x = small_shaft_length)
main_body = (
    small_shaft.faces(">X")
    .workplane()
    .circle(main_body_diameter / 2)
    .extrude(main_body_length)
)

# 3. Create the head (rightmost part), starting from the end of the main body
result = (
    main_body.faces(">X")
    .workplane()
    .circle(head_diameter / 2)
    .extrude(head_length)
)

# Alternatively, one could union three separate cylinders created at specific origins, 
# but the chaining method is more idiomatic for "extruding" shapes.