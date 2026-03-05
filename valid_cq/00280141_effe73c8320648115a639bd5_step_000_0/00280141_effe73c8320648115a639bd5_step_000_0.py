import cadquery as cq

# Parametric dimensions based on visual estimation
box_width = 50.0    # X dimension
box_depth = 50.0    # Y dimension
box_height = 25.0   # Z dimension
pin_diameter = 10.0
pin_length = 40.0

# Create the base geometry
# 1. Start with a box centered at the origin
# 2. Select the back face (>Y direction)
# 3. Create a workplane on that face (automatically centered)
# 4. Draw the circle for the pin
# 5. Extrude the pin outwards
result = (
    cq.Workplane("XY")
    .box(box_width, box_depth, box_height)
    .faces(">Y")
    .workplane()
    .circle(pin_diameter / 2.0)
    .extrude(pin_length)
)