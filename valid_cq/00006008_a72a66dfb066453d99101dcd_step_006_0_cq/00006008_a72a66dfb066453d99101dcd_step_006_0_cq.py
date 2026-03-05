import cadquery as cq

# Parameters for the curved block
inner_radius = 50.0  # Distance from center to the inner curved face
thickness = 20.0     # Radial thickness of the block
height = 30.0        # Vertical height of the block
angle = 45.0         # The angular span of the arc segment (in degrees)

# Calculate outer radius based on thickness
outer_radius = inner_radius + thickness

# Create the geometry
# Method: Sketch a 2D shape on the XY plane representing the base, then extrude it.
# The shape is a segment of an annulus (ring).

result = (
    cq.Workplane("XY")
    # Move to the starting point of the inner arc
    .moveTo(inner_radius, 0)
    # Draw a line out to the outer radius
    .lineTo(outer_radius, 0)
    # Draw the outer arc. 
    # The endpoint is calculated using simple trigonometry implicitly by revolve or explicitly via polar coordinates.
    # However, CadQuery's 2D engine is often easier with simple primitives or boolean operations.
    # Let's use a cleaner approach: Create a solid ring segment using revolution.
    
    # Alternative Approach (Revolution):
    # 1. Create a rectangle representing the cross-section on the XZ plane.
    # 2. Offset it from the Z-axis by the inner_radius.
    # 3. Revolve it around the Z-axis by the specified angle.
)

# Implementation of the Revolution Method (cleaner for arc segments):
result = (
    cq.Workplane("XZ")
    # Create a rectangle for the cross-section.
    # It is centered on X at (inner_radius + thickness/2) and Z at (height/2) usually,
    # or we can draw it from a corner.
    # Let's draw from the bottom-inner corner.
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, height)
    .lineTo(inner_radius, height)
    .close()
    # Revolve around the Z-axis (0,0,0) to (0,0,1)
    .revolve(angle, (0, 0, 0), (0, 0, 1))
)

# Export isn't requested, but creating the 'result' variable is.