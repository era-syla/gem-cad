import cadquery as cq

# Parametric dimensions for the U-shaped shim/bracket
thickness = 5.0          # Thickness of the plate
total_width = 40.0       # Outer width of the U-shape
slot_width = 20.0        # Inner width of the slot
leg_length = 60.0        # Length of the straight leg section

# Derived dimensions
outer_radius = total_width / 2.0
inner_radius = slot_width / 2.0

# Create the 3D model
# The geometry is constructed by sketching the 2D profile on the XY plane
# and extruding it. The arc center is placed at (0,0).
result = (
    cq.Workplane("XY")
    # Start at the top inner corner of the leg
    .moveTo(-leg_length, inner_radius)
    # Draw the straight inner edge to the start of the arc
    .lineTo(0, inner_radius)
    # Draw the inner semi-circle (180 degrees)
    .threePointArc((inner_radius, 0), (0, -inner_radius))
    # Draw the bottom inner straight edge
    .lineTo(-leg_length, -inner_radius)
    # Connect to the outer edge (leg end)
    .lineTo(-leg_length, -outer_radius)
    # Draw the bottom outer straight edge
    .lineTo(0, -outer_radius)
    # Draw the outer semi-circle (180 degrees)
    .threePointArc((outer_radius, 0), (0, outer_radius))
    # Draw the top outer straight edge
    .lineTo(-leg_length, outer_radius)
    # Close the profile
    .close()
    # Create the solid
    .extrude(thickness)
)