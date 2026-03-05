import cadquery as cq

# Model Parameters
thickness = 6.0        # Thickness of the strip material
width = 20.0           # Width of the strip (extrusion depth)
inner_radius = 45.0    # Radius of the inner curve
straight_length = 25.0 # Length of the straight leg sections

# Derived Parameter
outer_radius = inner_radius + thickness

# Generate the 3D Model
# Strategy: Create the "C" shape profile on the YZ plane and extrude it along the X axis.
result = (
    cq.Workplane("YZ")
    # Start at the end of the top inner straight section
    .moveTo(straight_length, inner_radius)
    
    # Draw the top inner straight line towards the center
    .lineTo(0, inner_radius)
    
    # Draw the inner semi-circle arc (180 degrees)
    # Starts at (0, r_in), passes through (-r_in, 0), ends at (0, -r_in)
    .threePointArc((-inner_radius, 0), (0, -inner_radius))
    
    # Draw the bottom inner straight line
    .lineTo(straight_length, -inner_radius)
    
    # Connect to the outer profile
    .lineTo(straight_length, -outer_radius)
    
    # Draw the bottom outer straight line
    .lineTo(0, -outer_radius)
    
    # Draw the outer semi-circle arc
    # Starts at (0, -r_out), passes through (-r_out, 0), ends at (0, r_out)
    .threePointArc((-outer_radius, 0), (0, outer_radius))
    
    # Draw the top outer straight line
    .lineTo(straight_length, outer_radius)
    
    # Close the wire to form the profile
    .close()
    
    # Extrude symmetrically to create the solid geometry
    .extrude(width, both=True)
)