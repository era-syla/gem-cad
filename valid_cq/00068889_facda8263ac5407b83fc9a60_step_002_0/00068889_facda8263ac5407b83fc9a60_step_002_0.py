import cadquery as cq

# Parametric dimensions based on visual estimation
length = 200.0          # Total length of the plate
width = 30.0            # Width of the plate
thickness = 3.0         # Thickness of the plate
notch_width = 2.0       # Width of the cutout slots
notch_depth = 6.0       # Depth of the cutout slots
end_offset = 30.0       # Distance from the ends to the outer notches

# Create the base rectangular board centered at the origin
# X-axis aligns with length, Y-axis with width, Z-axis with thickness
result = cq.Workplane("XY").box(length, width, thickness)

# Define notch configurations
# Format: (x_coordinate, side_factor)
# side_factor: -1 indicates the front edge (negative Y), 1 indicates the back edge (positive Y)
notch_configs = [
    (-(length / 2) + end_offset, -1),  # Left notch on the front edge
    (0, -1),                           # Middle notch on the front edge
    ((length / 2) - end_offset, 1)     # Right notch on the back edge
]

# Iterate through configurations to cut the notches
for x_pos, side in notch_configs:
    
    # Determine Y coordinate for the edge (front or back)
    y_edge = side * width / 2
    
    # Create a cutter solid
    # We define a rectangle centered on the edge. 
    # Height is set to notch_depth * 2 so that half of it cuts into the material by exactly notch_depth.
    cutter = (
        cq.Workplane("XY")
        .moveTo(x_pos, y_edge)
        .rect(notch_width, notch_depth * 2)
        .extrude(thickness * 2, both=True)  # Extrude taller than plate to ensure clean cut
    )
    
    # Subtract the cutter from the main body
    result = result.cut(cutter)