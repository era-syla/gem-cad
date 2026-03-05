import cadquery as cq

# Parametric dimensions
frame_width = 100.0   # Total width of the frame
frame_height = 80.0   # Total height of the frame
thickness = 5.0       # Thickness of the plate
frame_border = 10.0   # Width of the frame border (material thickness)
corner_radius = 3.0   # Radius for external corners

# Derived dimensions
inner_width = frame_width - (2 * frame_border)
inner_height = frame_height - (2 * frame_border)

# Create the main body
# 1. Start with a workplane
# 2. Sketch the outer rectangle
# 3. Sketch the inner rectangle (to create the hole)
# 4. Extrude the result
# 5. Apply fillets to vertical edges

result = (
    cq.Workplane("XY")
    .rect(frame_width, frame_height)
    .rect(inner_width, inner_height)
    .extrude(thickness)
    .edges("|Z")  # Select edges parallel to Z axis (vertical corners)
    .fillet(corner_radius)
)