import cadquery as cq

# Parametric dimensions based on the visual proportions of the image
length = 300.0        # Total length of the rail
height = 12.0         # Vertical height of the rail
thickness = 2.0       # Thickness of the material
notch_length = 35.0   # Length of the cutout section
notch_depth = 6.0     # Depth of the cutout from the top edge
tip_length = 3.0      # Length of the small tab/hook at the very end

# Create the model by drawing the side profile and extruding it
# Drawing starts at the bottom-left corner (0,0)
result = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(length, 0)                                          # Bottom edge
    .lineTo(length, height)                                     # Right end vertical edge
    .lineTo(length - tip_length, height)                        # Top of the end tab
    .lineTo(length - tip_length, height - notch_depth)          # Step down into the notch
    .lineTo(length - tip_length - notch_length, height - notch_depth) # Bottom horizontal of the notch
    .lineTo(length - tip_length - notch_length, height)         # Step up from the notch
    .lineTo(0, height)                                          # Top edge of the main body
    .close()                                                    # Close the profile (left edge)
    .extrude(thickness)                                         # Extrude to create the solid geometry
)