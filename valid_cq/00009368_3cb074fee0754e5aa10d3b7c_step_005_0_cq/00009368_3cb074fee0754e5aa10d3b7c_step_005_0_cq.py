import cadquery as cq

# --- Parameters ---
length = 1000.0  # Total length of the angle iron
leg1_length = 50.0  # Length of the first leg (vertical)
leg2_length = 50.0  # Length of the second leg (horizontal)
thickness = 5.0     # Thickness of the material

# --- Modeling ---

# We will create the L-profile cross-section and extrude it.
# The profile is sketched on the XY plane.

# Start a new workplane
result = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    # Draw the outer L-shape
    .lineTo(0, leg1_length)         # Go up
    .lineTo(thickness, leg1_length) # Go right (top thickness)
    .lineTo(thickness, thickness)   # Go down to inner corner top
    .lineTo(leg2_length, thickness) # Go right to end of horiz leg
    .lineTo(leg2_length, 0)         # Go down to origin level
    .close()                        # Close back to (0,0)
    # Extrude to create the 3D solid
    .extrude(length)
)

# Optional: Add fillets to the inner corner if desired (standard structural angles often have a fillet)
# result = result.faces("|Z").edges(cq.selectors.NearestToPointSelector((thickness, thickness))).fillet(thickness/2)

# Export (if needed, but the prompt asks for the variable 'result')
# cq.exporters.export(result, "angle_iron.step")