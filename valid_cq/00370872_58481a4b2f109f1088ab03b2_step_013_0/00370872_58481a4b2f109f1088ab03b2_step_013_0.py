import cadquery as cq

# Parametric dimensions based on visual proportions
main_rod_length = 100.0       # Length of the long diagonal rod
main_rod_diameter = 2.0       # Diameter of the rods (thin wireframe look)
vertical_rod_height = 40.0    # Height of the vertical post
junction_position = 0.4       # Normalized position of the vertical rod along the main rod (0.0 to 1.0)

# Calculate start position for the main rod to align the intersection at the origin
# The main rod is aligned along the Y-axis to match the isometric view direction (bottom-left to top-right)
y_start_offset = -main_rod_length * junction_position

# Create the main rod (diagonal in ISO view)
# We use the XZ plane which has a normal along the Y-axis
main_rod = (
    cq.Workplane("XZ")
    .circle(main_rod_diameter / 2.0)
    .extrude(main_rod_length)
    .translate((0, y_start_offset, 0))
)

# Create the vertical rod
# Aligned with the Z-axis, starting from the origin (intersection point)
vertical_rod = (
    cq.Workplane("XY")
    .circle(main_rod_diameter / 2.0)
    .extrude(vertical_rod_height)
)

# Combine the parts into the final result
result = main_rod.union(vertical_rod)