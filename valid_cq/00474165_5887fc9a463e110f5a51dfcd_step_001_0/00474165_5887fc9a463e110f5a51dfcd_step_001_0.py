import cadquery as cq

# Parametric dimensions describing the geometry
total_length = 100.0       # Total length along X axis
width_center = 50.0        # Maximum width at the center (bulge)
width_ends = 30.0          # Width at the flat ends
hole_diameter = 20.0       # Diameter of the central hole
thickness = 3.0            # Thickness of the plate

# Helper calculations for geometry points
x_half = total_length / 2.0
y_end_half = width_ends / 2.0
y_center_half = width_center / 2.0

# Calculate relative vectors for the 3-point arcs
# Top Arc: Start -> Mid -> End
# Start is Top-Left corner
# Mid is Top-Center
# End is Top-Right corner
top_arc_mid_rel = (x_half, y_center_half - y_end_half)
top_arc_end_rel = (total_length, 0)

# Bottom Arc: Start -> Mid -> End
# Start is Bottom-Right corner
# Mid is Bottom-Center
# End is Bottom-Left corner
bot_arc_mid_rel = (-x_half, -(y_center_half - y_end_half))
bot_arc_end_rel = (-total_length, 0)

# Generate the 3D model
result = (
    cq.Workplane("XY")
    # Start drawing the outer profile from the top-left corner
    .moveTo(-x_half, y_end_half)
    
    # Create the top curved edge
    .threePointArc(top_arc_mid_rel, top_arc_end_rel)
    
    # Create the straight right edge
    .lineTo(0, -width_ends)
    
    # Create the bottom curved edge
    .threePointArc(bot_arc_mid_rel, bot_arc_end_rel)
    
    # Close the wire to create the left edge
    .close()
    
    # Create the central hole profile within the same sketch
    .circle(hole_diameter / 2.0)
    
    # Extrude the sketch to create the solid
    .extrude(thickness)
)