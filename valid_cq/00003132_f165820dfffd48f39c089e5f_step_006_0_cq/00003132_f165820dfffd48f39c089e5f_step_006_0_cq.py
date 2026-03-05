import cadquery as cq

# Parametric dimensions
box_width = 100.0   # Width of the main body (X axis)
box_depth = 80.0    # Depth of the main body (Y axis)
box_height = 90.0   # Height of the main body (Z axis)

leg_size = 5.0      # Width/Depth of the square legs
leg_height = 10.0   # Height of the legs
leg_inset = 2.0     # Distance from the edge for the legs

# Create the main body
main_body = cq.Workplane("XY").box(box_width, box_depth, box_height)

# Calculate leg positions relative to center
x_offset = (box_width / 2) - (leg_size / 2) - leg_inset
y_offset = (box_depth / 2) - (leg_size / 2) - leg_inset

# Create the legs
# We select the bottom face of the main body
# Then we draw four rectangles for the legs and extrude them downwards
result = (
    main_body
    .faces("<Z")
    .workplane()
    .rect(leg_size, leg_size, forConstruction=True) # Center reference
    .pushPoints([
        (x_offset, y_offset),
        (x_offset, -y_offset),
        (-x_offset, y_offset),
        (-x_offset, -y_offset)
    ])
    .rect(leg_size, leg_size)
    .extrude(leg_height)
)