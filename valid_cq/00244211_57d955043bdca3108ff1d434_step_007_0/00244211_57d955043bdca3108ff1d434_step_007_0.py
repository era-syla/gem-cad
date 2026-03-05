import cadquery as cq

# Parameter definitions based on the visual proportions of the image
# The part appears to be a long, thin rail or bracket with relief cuts on the bottom
length = 400.0        # Total length of the part
height = 25.0         # Overall height at the ends
thickness = 5.0       # Material thickness (depth)
end_tab_width = 30.0  # Width of the 'legs' or tabs at the ends
cutout_height = 12.0  # Height of the rectangular recess in the bottom center

# Create the 3D model
# We draw the profile on the XZ plane (Front view) and extrude along Y (Thickness)
result = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(end_tab_width, 0)                   # Bottom of the left leg
    .lineTo(end_tab_width, cutout_height)       # Step up to the cutout
    .lineTo(length - end_tab_width, cutout_height) # Across the main span
    .lineTo(length - end_tab_width, 0)          # Step down to the right leg
    .lineTo(length, 0)                          # Bottom of the right leg
    .lineTo(length, height)                     # Right vertical edge
    .lineTo(0, height)                          # Top straight edge
    .close()                                    # Close the profile back to origin
    .extrude(thickness)                         # Create the solid geometry
)